import os
import pickle
import time
from typing import List
from typing import Tuple

import click
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as st
import seaborn as sns
from sklearn.feature_selection import SelectKBest
from sklearn.metrics import pairwise_distances
from tqdm.autonotebook import tqdm


class Model:
    def __init__(self, opts):
        # Convert all opts attributes to self attributes
        self.opts = opts
        self.__dict__.update(vars(opts))
        # Load input data
        self.df = self.load_df(self.background_path)
        self.sample = self.get_sample()
        self.df = self.df.sort_values(self.group)
        self.genes = self.get_genes()
        # Calculate/save ranks and establish initial conditions for run
        self.ranks = self.anova_distances()
        self.n_bg = min(opts.n_bg, len(self.ranks))
        self.initial_genes = self.parse_gene_list()
        self.pval_runs = pd.DataFrame()
        self.pearson_correlations = []
        # Attributes that will change based on number of background datasets in that run
        # self.select_training_set and self.select_training_genes need to be run before self.run_model
        self.training_set = None
        self.training_genes = None
        self.backgrounds = None
        self.index_df = None
        self.x_ix = None
        self.s_map = None
        self.s_ix = None
        self.trace = None
        self.model = None
        self.weights = None
        self.ppc = None
        self.ppp = None

    @staticmethod
    def load_df(df_path: str) -> pd.DataFrame:
        """
        Load background DataFrame

        Args:
            df_path: Path to DataFrame

        Returns:
            Background DataFrame
        """
        if df_path.endswith(".csv"):
            df = pd.read_csv(df_path, index_col=0)
        elif df_path.endswith(".tsv"):
            df = pd.read_csv(df_path, sep="\t", index_col=0)
        else:
            try:
                df = pd.read_hdf(df_path)
            except Exception as e:
                print(e)
                raise RuntimeError(f"Failed to open DataFrame: {df_path}")
        return df

    def get_sample(self) -> pd.Series:
        """Loads DataFrame containing sample and returns sample"""
        df = self.load_df(self.sample_path)
        if self.name in df.index:
            return df.loc[self.name]
        else:
            msg = f"Sample {self.name} not located in index of DataFrame {self.background_path}"
            raise RuntimeError(msg)

    def get_genes(self) -> List[str]:
        """Gets gene list from background and checks against input"""
        bg_genes = self.df.columns[self.col_skip :]
        sample_genes = self.sample.index
        genes = [x for x in bg_genes if x in sample_genes]
        if len(genes) != len(bg_genes):
            msg = "WARNING: Genes do not match between input and background DataFrame"
            click.secho(msg, fg="yellow")
            diff = set(bg_genes).symmetric_difference(sample_genes)
            click.secho(f"WARNING: {len(diff)} genes do not match", fg="yellow")
        return genes

    def select_k_best_genes(self, df, n=50) -> List[str]:
        """
        Select K genes from background dataset based on ANOVA F-value of groups

        Args:
            df: Input DataFrame to run ANOVA on
            n: Number of genes to select (k)

        Returns:
            List of selected genes
        """
        k = SelectKBest(k=n)
        k.fit_transform(df[self.genes], df[self.group])
        return [self.genes[i] for i in k.get_support(indices=True)]

    def anova_distances(self, percent_genes=0.10):
        """
        Calculates distance to each group via pairwise distance using top N ANOVA genes

        Args:
            percent_genes: Percent of ANOVA genes to use for pairwise distance

        Returns:
            DataFrame of pairwise distances
        """
        click.echo(f"Ranking background datasets by {self.group} via ANOVA")
        n_genes = int(percent_genes * len(self.genes))
        skb_genes = self.select_k_best_genes(self.df, n=n_genes)
        dist = pairwise_distances(
            np.array(self.sample[skb_genes]).reshape(1, -1), self.df[skb_genes]
        )
        dist = pd.DataFrame([dist.ravel(), self.df["tissue"]]).T
        dist.columns = ["Distance", "Group"]

        # Median by group and sort
        med_dist = (
            dist.groupby("Group").apply(lambda x: x["Distance"].median()).reset_index()
        )
        med_dist.columns = ["Group", "MedianDistance"]
        med_dist = med_dist.sort_values("MedianDistance").reset_index(drop=True)
        for i in range(min(5, len(med_dist))):
            click.echo(f"\t{i + 1}.\t{med_dist.iloc[i].Group}")
        return med_dist

    def save_ranks(self):
        """Convenience method to save rank information"""
        ranks_out = os.path.join(self.out_dir, "ranks.tsv")
        self.ranks.to_csv(ranks_out, sep="\t")

    def parse_gene_list(self) -> List[str]:
        """
        Parse gene list if provided, otherwise select some genes via ANOVA

        Returns:
            List of initial genes
        """
        if self.gene_list is None:
            msg = f"No gene list provided which is unusual - check command line. "
            msg += f"Selecting {self.n_train} genes via SelectKBest (ANOVA F-value)"
            click.secho(msg, fg="yellow")
            # Select genes based on maximum number of background datasets
            genes = self.select_k_best_genes(self.df, n=self.n_train)
        else:
            with open(self.gene_list, "r") as f:
                initial_genes = [x.strip() for x in f.readlines() if not x.isspace()]
                genes = [x for x in initial_genes if x in self.genes]
                if len(initial_genes) != len(genes):
                    diff = set(initial_genes).difference(genes)
                    msg = f"WARNING: Gene list contains genes not in the input: {diff}"
                    click.secho(msg, fg="yellow")
        return genes

    def select_training_set(self, num_backgrounds):
        """Select training subset from entire background dataset"""
        top_groups = self.ranks.head(num_backgrounds)["Group"]
        group_msg = "\t".join(top_groups)
        click.secho(f"Running with groups: {group_msg}")
        train_set = self.df[self.df[self.group].isin(top_groups)]
        self.training_set = train_set.sort_values(self.group)
        self.backgrounds = sorted(self.training_set[self.group].unique())

    def select_training_genes(self):
        """Select complete training gene set based on `initial_genes` and `max_genes`"""
        if len(self.initial_genes) < self.max_genes:
            diff = int(len(self.initial_genes) * 0.30)
            diff = min(diff, self.max_genes - len(self.initial_genes))
            total = len(self.initial_genes) + diff
            msg = f"Adding {diff} genes (30% more) via ANOVA F-value to reach {total} genes for model calibration."
            click.secho(msg, fg="yellow")
            training_genes = self.initial_genes + self.select_k_best_genes(
                self.training_set, n=diff
            )
            training_genes = sorted(set(training_genes))
        else:
            training_genes = self.initial_genes
        self.training_genes = training_genes

    def create_index_dataframe(self):
        """Creates DataFrame used to index X_{d,g} RVs to observed values"""
        xdf = self.training_set[["tissue"] + self.training_genes].melt(id_vars="tissue")
        xdf["gt"] = xdf.variable + "__" + xdf.tissue
        xdf["gt"] = xdf["gt"].astype("category")
        xdf["group"] = xdf.tissue.astype("category")
        xdf["variable"] = xdf.variable.astype("category")
        self.index_df = xdf.sort_values(["variable", "group"])

    def create_category_indexers(self):
        """Categorical index maps and the index vectors for observed variables"""
        # Index vectors for mapping observed values to RVs (see model)
        self.x_ix = self.index_df["gt"].cat.codes.values
        self.s_ix = list(range(len(self.training_genes)))

        # Mapping index back to the training genes
        self.s_map = {v: k for k, v in dict(enumerate(self.training_genes)).items()}

    def run_model(self, **kwargs):
        """Run Bayesian model using prefit Y's for each Gene and Dataset distribution"""
        # Importing here since Theano base_compiledir needs to be set prior to import
        import pymc3 as pm

        click.echo("Building model")
        with pm.Model() as self.model:
            # Constants
            N = len(self.backgrounds)
            M = len(self.training_genes)
            MN = M * N

            # Prior constants
            mu_exp = self.df[self.training_genes].mean().mean()
            sd_exp = self.df[self.training_genes].std().mean()

            # Gene Model Priors
            gm_sd = pm.InverseGamma("gm_sd", 1, 1, shape=MN)
            gm_mu = pm.Normal("gm_mu", mu_exp, sd_exp, shape=MN)

            # Gene model
            pm.Normal(
                "x_hat",
                mu=gm_mu[self.x_ix],
                sd=gm_sd[self.x_ix],
                shape=MN,
                observed=self.index_df.value,
            )
            x = pm.Normal("x", mu=gm_mu, sd=gm_sd, shape=MN)

            # Likelihood priors
            eps = pm.InverseGamma("eps", 1, 1)
            if N == 1:
                beta = [1]
            else:
                beta = pm.Dirichlet("beta", a=np.ones(N))

            # Likelihood
            norm = np.zeros(M)
            gm_sd_2d = gm_sd.reshape((M, N))
            for i in range(N):
                norm += beta[i] / gm_sd_2d[:, i]
            norm = pm.Deterministic("norm", norm)

            y = pm.Deterministic("y", pm.math.dot((x / gm_sd).reshape((M, N)), beta))
            norm_eps = pm.Deterministic("norm_eps", eps / norm)
            sample_genes = self.sample[self.training_genes].values
            pm.Laplace(
                "y_hat", mu=(y / norm)[self.s_ix], b=norm_eps, observed=sample_genes
            )

            trace = pm.sample(**kwargs)
        self.trace = trace
        click.echo("Calculating posterior predictive samples")
        self.ppc = pm.sample_posterior_predictive(trace, model=self.model)

    def posterior_predictive_pvals(self):
        """Produces Series of posterior p-values for all genes in the Posterior Predictive Check (PPC) dictionary"""
        click.echo("Calculating p-values")
        pvals = {}
        for gene in tqdm(self.initial_genes):
            yx = self.s_map[gene]
            post = self.ppc["y_hat"][:, yx]
            pval = len([x for x in post if x > self.sample[gene]]) / len(post)
            pvals[gene] = round(pval, 3)

        self.ppp = pd.DataFrame(pvals.items(), columns=["Gene", "Pval"]).sort_values(
            "Pval"
        )
        self.ppp = self.ppp.set_index("Gene", drop=True)

    def update_pvals(self):
        """Update per-run p-values"""
        self.pval_runs = pd.concat(
            [self.pval_runs, self.ppp], axis=1, sort=True
        ).dropna()
        self.pval_runs.columns = list(range(len(self.pval_runs.columns)))

    def save_pval_runs(self):
        """Save p-values for each run"""
        pval_runs_out = os.path.join(self.out_dir, "_pval_runs.tsv")
        self.pval_runs.to_csv(pval_runs_out, sep="\t")

    def update_pearson_correlations(self):
        """Update Pearson correlations between runs"""
        if len(self.pval_runs.columns) < 2:
            return
        x, y = self.pval_runs.columns[-2:]
        pr, _ = st.pearsonr(self.pval_runs[x], self.pval_runs[y])
        self.pearson_correlations.append(str(pr))
        return pr

    def save_pearson_correlations(self):
        """Save Pearson correlations"""
        if not self.pearson_correlations:
            return
        pearson_out = os.path.join(self.out_dir, "_pearson_correlations.txt")
        with open(pearson_out, "w") as f:
            f.write("\n".join(self.pearson_correlations))

    def calculate_weights(self):
        """Calculates weights of the background groups by examining the beta coefficient in the trace"""
        class_col = []
        for c in self.backgrounds:
            class_col.extend([c for _ in range(len(self.trace["eps"]))])

        weight_by_class = pd.DataFrame(
            {
                "Class": class_col,
                "Weights": np.array(
                    [self.trace["beta"][:, x] for x in range(len(self.backgrounds))]
                ).ravel(),
            }
        )
        self.weights = weight_by_class

    def plot_weights(self):
        """Plot model coefficients associated with each group"""
        output = os.path.join(self.out_dir, "weights.png")
        plt.figure(figsize=(12, 4))
        sns.boxplot(data=self.weights, x="Class", y="Weights")
        plt.xticks(rotation=90)
        plt.title("Median Beta Coefficient Weight by Tissue for N-of-1 Sample")
        if output:
            plt.savefig(output, bbox_inches="tight")

    def save_weights(self) -> None:
        """Save weights as both a table and plot"""
        if self.weights is None:
            self.calculate_weights()
        self.plot_weights()
        # Convert weights to summarized information of median and std
        weights = self.weights.groupby("Class").agg({"Weights": ["median", "std"]})
        weights = weights.sort_values(("Weights", "median"), ascending=False)
        weights.columns = ["Median", "std"]
        weights.index.name = None
        weights.to_csv(os.path.join(self.out_dir, "weights.tsv"), sep="\t")

    def save_traceplot(self):
        """Saves traceplot of PyMC3 run"""
        import pymc3 as pm

        # 'b' parameter is not in the model if n_bg == 1
        b = True if self.n_bg > 1 else False
        varnames = ["beta", "eps"] if b else ["eps"]
        pm.traceplot(self.trace, var_names=varnames)
        traceplot_out = os.path.join(self.out_dir, "traceplot.png")
        fig = plt.gcf()
        fig.savefig(traceplot_out)

    def save_pvalues(self):
        """Save p-values for the final run"""
        ppp_out = os.path.join(self.out_dir, "pvals.tsv")
        self.ppp.columns = ["Up-pvalue"]
        self.ppp["Down-pvalue"] = 1 - self.ppp["Up-pvalue"]
        self.ppp["Down-pvalue"] = self.ppp["Down-pvalue"].round(3)
        self.ppp.to_csv(ppp_out, sep="\t")

    def output_run_info(self, runtime, unit):
        """Save output run information"""
        run_path = os.path.join(self.out_dir, "_run_info.tsv")
        with open(run_path, "w") as f:
            for k in vars(self.opts):
                f.write(f"{k}\t{getattr(self.opts, k)}\n")
            f.write(f"Runtime\t{runtime} {unit}\n")
            # Add model error
            err_med = np.median(self.trace["eps"])
            err_std = np.std(self.trace["eps"])
            f.write(f"epsilon_median\t{err_med}\n")
            f.write(f"epsilon_std\t{err_std}\n")

    def save_gelman_rubin(self):
        """Saves Gelman-Rubin statistics for the final run"""
        import pymc3 as pm

        out = os.path.join(self.out_dir, "_gelman-rubin.tsv")
        stats = []
        with open(out, "w") as f:
            for k, v in pm.stats.rhat(self.trace).items():
                try:
                    stats.extend([float(x) for x in v])
                    v_out = "\t".join([str(float(x)) for x in v])
                except TypeError:
                    stats.append(float(v))
                    v_out = v
                f.write(f"{k}\t{v_out}\n")
            median = round(np.median(stats), 5)
            f.write(f"Median\t{median}\n")
            if 0.8 < median < 1.2:
                click.secho(
                    f"Model converged with Gelman-Rubin of {median}", fg="green"
                )
            else:
                click.secho(
                    f"Model encountered difficulties converging with Gelman-Rubin of {median}. "
                    f"Should be close to 1.0",
                    fg="yellow",
                )

    def pickle_model(self):
        """Pickles PyMC3 model and trace"""
        model_out = os.path.join(self.out_dir, "model.pkl")
        with open(model_out, "wb") as buff:
            pickle.dump({"model": self.model, "trace": self.trace}, buff)

    @staticmethod
    def display_runtime(t0: float, total: bool = False) -> Tuple[float, str]:
        """
        Displays runtime given an initial timepoint

        Args:
            t0: The initial time point generated via time.time()
            total: If this constitutes the total runtime over all models

        Returns:
            runtime and unit of the runtime (min / hr)
        """
        runtime = round((time.time() - t0) / 60, 2)
        unit = "min" if runtime < 60 else "hr"
        runtime = runtime if runtime < 60 else round(runtime / 60, 2)
        msg = "Total runtime over all models" if total else "Model runtime"
        click.secho(f"{msg}: {runtime} ({unit})", fg="green")
        return runtime, unit
