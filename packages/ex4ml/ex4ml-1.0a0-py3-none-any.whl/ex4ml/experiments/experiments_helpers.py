"""Helpers for experiment files
"""

from scipy.stats import ttest_ind


def calculate_p_value(row, base_view_name, results):
    """
    Calculates the p-value for the hypothesis test that the mean scores for a view is equal to the mean score for the
    base view.

    Args:
        row (pandas.DataFrame): The row containing results for a single grid search.
        base_view_name (str): The name of the baseline view.
        results (pandas.DataFrame): The ``DataFrame`` containing results from all estimator and view pairs.

    Returns:
        str: A string representation of the p-value.
    """

    # Display dash if base view is under consideration.
    if base_view_name == row["View"]:
        return 0.0

    # Get current row scores and base row scores.
    comp_scores = row["scores"]
    base_scores = (
        results[(results["View"] == base_view_name) & (
            results["Estimator"] == row["Estimator"])]
        .iloc[0]["scores"]
    )

    # Calculate test statistic and p-value.
    _, p_val = ttest_ind(comp_scores, base_scores)
    return p_val
