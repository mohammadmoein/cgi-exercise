from sklearn.preprocessing import StandardScaler
from sklearn.metrics import balanced_accuracy_score

import pandas as pd
from typing import List, Dict
from sklearn.model_selection import RandomizedSearchCV
from sklearn.pipeline import Pipeline
import sklearn.base
from loguru import logger
import pickle
from pathlib import Path
import json
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(train_csv_path, test_csv_path, targets):
    train_df = pd.read_csv(train_csv_path)
    test_df = pd.read_csv(test_csv_path)
    feature_columns = train_df.columns.difference(targets)
    train_x, train_y = train_df[feature_columns], train_df[targets]
    test_x, test_y = test_df[feature_columns], test_df[targets]
    return (train_x, train_y, test_x, test_y)


def train_model(
    clf: sklearn.base.ClassifierMixin,
    train_x,
    train_y,
    hparams: Dict,
    cv=2,
):
    pipe = Pipeline(steps=[("scaler", StandardScaler()), ("model", clf())])
    hparams = {f"model__{key}": val for key, val in hparams.items()}
    search = RandomizedSearchCV(
        estimator=pipe,
        param_distributions=hparams,
        scoring='balanced_accuracy',
        refit="True",
        cv=cv,
    )
    search.fit(train_x, train_y)
    return search


def log_model(result, dest_path: Path, clf_name, target, meta_data,cm):
    score_df = pd.DataFrame(result.cv_results_)
    best_model = result.best_estimator_
    dest_dir = dest_path.joinpath(clf_name).joinpath(target)
    dest_dir.mkdir(exist_ok=True, parents=True)
    score_df.to_csv(dest_dir.joinpath("cv_results.csv"), index=False)
    with open(dest_dir.joinpath("model.pkl"), "wb") as f:
        pickle.dump(best_model, f)
    json.dump(meta_data, open(dest_dir.joinpath("meta_data.json"), "w"))

    disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                        display_labels=result.best_estimator_.classes_)

    fig = plt.figure(figsize=(15,15))
    if cm.shape[0]>25:
        sns.heatmap(cm,cmap='crest',ax=fig.gca(),xticklabels=result.best_estimator_.classes_, yticklabels=result.best_estimator_.classes_,)
    else:
        disp.plot(ax=plt.gca(),xticks_rotation='vertical')
    fig.savefig(dest_dir.joinpath('confusion_matrix.png'))
    


def build_train_model(
    clf,
    train_csv_path,
    test_csv_path,
    targets,
    hparams,
    cv,
    dest_path,
):
    train_x, train_y, test_x, test_y = load_data(train_csv_path, test_csv_path, targets)
    for t_name in targets:

        result = train_model(
            clf, train_x, train_y[t_name].to_numpy(), hparams, cv
        )
        pred = result.predict(test_x)
        performance = balanced_accuracy_score(y_true=test_y[t_name].to_numpy(), y_pred= pred)
        meta_data = {
            f"{t_name}_test_performance": performance,
            "train_csv": train_csv_path.__str__(),
            "test_csv": test_csv_path.__str__(),
            "target": t_name,
        }
        cm = confusion_matrix(test_y[t_name].to_numpy(), pred, labels=result.best_estimator_.classes_)
 

        log_model(result, dest_path, clf().__class__.__name__, t_name, meta_data,cm)
        logger.debug(f'{t_name}: model is trianed')