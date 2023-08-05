"""Methods for running machine learning experiments.
"""

import pandas as pd
from sklearn.model_selection import GridSearchCV
from ex4ml.experiments.experiments_helpers import calculate_p_value


def run_prediction_experiment(view, target, estimators, scoring):
    """
    Run supervised learning experiments comparing multiple estimators' target prediction on a particular view.

    Args:
        view (iterable): The view with the features to use for prediction.
        target (iterable): The target to predict from the view.
        estimators (iterable): An iterable of dictionaries where each element is of the form:
            ``{'name': estimator_name, 'estimator': estimator, 'parameters': param_grid}``.
        scoring (str or sklearn.scorer): The scoring method for running the grid search.

    Returns:
        pandas.DataFrame: A ``DataFrame`` containing the results for each estimator in the experiment.
    """

    # Perform the grid search per estimator and get the list of resulting
    # best estimators and grid search results.
    best_estimators = [
        GridSearchCV(estimator["estimator"],
                     estimator["parameters"], scoring=scoring)
        .fit(view, target) for estimator in estimators
    ]

    # Place the results for the experiment in a well organized DataFrame.
    score_scalar = -1 if "neg" in scoring else 1
    results = pd.DataFrame([
        {
            "Estimator": estimator["name"],
            "Score": best_estimators[i].best_score_ * score_scalar,
            "Std Dev": best_estimators[i].cv_results_['std_test_score'][best_estimators[i].best_index_],
            "est": best_estimators[i].best_estimator_,
            "params": best_estimators[i].best_params_,
            "scores": [best_estimators[i].cv_results_[split][best_estimators[i].best_index_] * score_scalar
                       for split in best_estimators[i].cv_results_ if 'test_score' in split and 'split' in split]
        } for i, estimator in enumerate(estimators)
    ])

    # Return all results.
    return results


def run_prediction_view_comparison(views, target, estimators, scoring, base_view_name=None):
    """
    Run supervised learning experiments comparing multiple estimators' target prediction using multiple views.

    Args:
        views (dict): The views with the features to use for prediction. Has the form:
            ``{'view1': data1, 'view2': data2, ...}``.
        target (iterable): The target to predict from each view.
        estimators (iterable): An iterable of dictionaries where each element is of the form:
            ``{'name': estimator_name, 'estimator': estimator, 'parameters': param_grid}``.
        scoring (str or sklearn.scorer): The scoring method for running the grid search.
        base_view_name (str, optional): The name of the view to consider the base on for reporting p-values. Defaults to
            ``None``.

    Returns:
        pandas.DataFrame: A ``DataFrame`` containing the results for each estimator and view in the experiment.
    """

    # Catalog the list of views and perform a single-view experiment for each.
    view_names = list(views.keys())
    extracted_results = [run_prediction_experiment(views[view_name], target, estimators, scoring)
                         for view_name in view_names]
    results = None

    # Put together results into combined DataFrame.
    for i, data_frame in enumerate(extracted_results):
        data_frame.insert(loc=0, column="View",
                          value=[view_names[i]] * len(data_frame.index))
        if results is not None:
            results = results.append(data_frame)
        else:
            results = data_frame

    if base_view_name is not None:
        # Calculate p-values.
        results["p-Value"] = results.apply(
            calculate_p_value, axis=1, args=(base_view_name, results))

    # Return all results.
    return results
