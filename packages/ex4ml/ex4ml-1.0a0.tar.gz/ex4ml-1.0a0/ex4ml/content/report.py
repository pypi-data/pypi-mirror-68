"""Contains classes and functions to transform outputs from experiments into paper content."""


def results_to_latex(results, sd_range=2.0):
    """
    Convert results from an ML experiment into a LaTeX tabular format.

    Args:
        results (pandas.DataFrame): The results from an ML experiment.
        sd_range (float, optional): The scalar to apply to the standard deviation for the range of each score.

    Returns:
        str: A LaTeX table generated for the results of all estimators and all views in the experiment.
    """

    # If results are single-view, we only need a simple table with estimators as labels.
    if "View" not in results.columns:
        filtered_results = results[["Estimator"]]
        filtered_results.loc[:, "Score"] = results.apply(
            lambda row: f"${row['Score']:.3f} \\pm {sd_range * row['Std Dev']:.3f}$",
            axis=1)
        return filtered_results.to_latex(index=False, escape=False)

    # Results are multiple-view, we need a table with rows as views and columns as estimators.
    filtered_results = results[["Estimator", "View"]]

    # If we are given a p-value, write it in to the scores.
    if "p-Value" in results.columns:
        filtered_results.loc[:, "Score"] = results.apply(
            lambda row: (
                f"${row['Score']:.3f} \\pm {sd_range * row['Std Dev']:.3f} " +
                (f"({row['p-Value']:.3f})" if row['p-Value'] > 0.0 else "(-)") + "$"
            ),
            axis=1)
    else:
        filtered_results.loc[:, "Score"] = results.apply(
            lambda row: f"${row['Score']:.3f} \\pm {sd_range * row['Std Dev']:.3f}$",
            axis=1)

    filtered_results = filtered_results.pivot(index="View", columns="Estimator", values="Score")
    return filtered_results.to_latex(escape=False)
