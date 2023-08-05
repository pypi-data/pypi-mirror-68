""" Unsupervised learning experiment code
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV, ParameterGrid, KFold
from ex4ml.experiments.experiments_helpers import calculate_p_value


def run_clustering_experiment(view, clustering_methods, scoring, known_labels=None):
    """
    Run a clustering experiment with a single view and multiple models.

    Args:
        view (iterable): The list of features to use for each sample.
        clustering_methods (list): Dictionaries of clustering method names, models, and params to search.
        scoring (sklearn.Scorer or str): sklearn scoring method or string from predefined ones.
        known_labels (iterable, optional): The known labels for the view if available. Defaults to ``None``.

    Returns:
        pandas.DataFrame: The results of the experiment in table form.
    """
    if known_labels is not None:
        best_estimators = [GridSearchCV(each_clustering_method["estimator"], each_clustering_method["parameters"],
                                        scoring=scoring, n_jobs=-1).fit(view, known_labels)
                           for each_clustering_method in clustering_methods]
        # Place the results for the experiment in a well organized DataFrame.
        all_results = pd.DataFrame([
            {
                "Estimator": estimator["name"],
                "Score": best_estimators[i].best_score_,
                "Std Dev": best_estimators[i].cv_results_['std_test_score'][best_estimators[i].best_index_],
                "est": best_estimators[i].best_estimator_,
                "params": best_estimators[i].best_params_,
                "scores": [best_estimators[i].cv_results_[split][best_estimators[i].best_index_]
                           for split in best_estimators[i].cv_results_ if 'test_score' in split and 'split' in split]
            } for i, estimator in enumerate(clustering_methods)
        ])
    else:
        n_splits = 10
        best_estimators = []
        best_estimators_results = []
        for each_clustering_method in clustering_methods:
            best_params = {}
            best_score = float("-inf")
            best_scores = []
            for parameters in ParameterGrid(each_clustering_method["parameters"]):
                scores = []
                k_fold = KFold(n_splits=n_splits, shuffle=True)
                for train, valid in k_fold.split(view):
                    estimator = each_clustering_method["estimator"].set_params(**parameters)
                    estimator.fit(view[train])
                    try:
                        scores.append(scoring(view[valid], estimator.predict(view[valid])))
                    except ValueError as error:
                        print("WARNING. Error occurred with calculation")
                        print(error)
                        scores.append(0)
                current_score = sum(scores)/n_splits
                if current_score > best_score:
                    best_params = parameters
                    best_score = current_score
                    best_scores = scores
            best_estimator = each_clustering_method["estimator"].set_params(**best_params).fit(view)
            best_estimators.append(best_estimator)
            best_estimators_results.append({
                "std_test_score": np.std(best_scores),
                "scores": best_scores,
                "mean": best_score,
                "params": best_params
            })

        all_results = pd.DataFrame([
            {
                "Estimator": estimator["name"],
                "Score": best_estimators_results[i]["mean"],
                "Std Dev": best_estimators_results[i]["std_test_score"],
                "est": best_estimators[i],
                "params": best_estimators_results[i]["params"],
                "scores": best_estimators_results[i]["scores"]
            } for i, estimator in enumerate(clustering_methods)
        ])

    return all_results


def run_clustering_view_comparison(views, clustering_methods, scoring, known_labels=None, base_view_name=None):
    """
    Run a clustering experiment with multiple views and multiple models, comparing the view results.

    Args:
        views (dictionary): A dictionary with view names and view values.
        clustering_methods (list): Dictionaries of clustering method names, models, and params to search.
        scoring (sklearn.Scorer or str): Sklearn scoring method or string from predefined ones.
        known_labels (iterable, optional): The known labels for the view if available. Defaults to ``None``.
        base_view_name (str, optional): The name of the view to consider the base on for reporting p-values. Defaults to
            ``None``.

    Returns:
        pandas.DataFrame: The results of the experiment in table form comparing all views with each method.
    """

    # Catalog the list of views and perform a single-view experiment for each.
    view_names = list(views.keys())
    extracted_results = [run_clustering_experiment(
        views[view_name], clustering_methods, scoring, known_labels) for view_name in view_names]

    all_results = None

    # Put together results into combined DataFrame.
    for i, data_frame in enumerate(extracted_results):
        data_frame.insert(loc=0, column="View", value=[
                          view_names[i]] * len(data_frame.index))
        if all_results is not None:
            all_results = all_results.append(data_frame)
        else:
            all_results = data_frame

    if base_view_name is not None:
        # Calculate p-values.
        all_results["p-Value"] = all_results.apply(
            calculate_p_value, axis=1, args=(base_view_name, all_results))

        # Copy view and estimator from all results.
        # Add value column that is score in form: SCORE +- 2 * STD DEV (P)
        results = all_results[["View", "Estimator"]]
        results["Value"] = all_results.apply(
            lambda x: f"${x['Score']:.3f} \\pm {2 * x['Std Dev']:.3f} ({x['p-Value']})$", axis=1)
    else:
        # Copy view and estimator from all results.
        # Add value column that is score in form: SCORE +- 2 * STD DEV
        results = all_results[["View", "Estimator"]]
        results["Value"] = all_results.apply(
            lambda x: f"${x['Score']:.3f} \\pm {2 * x['Std Dev']:.3f}$", axis=1)

    results = results.pivot(index="View", columns="Estimator", values="Value")
    return results
