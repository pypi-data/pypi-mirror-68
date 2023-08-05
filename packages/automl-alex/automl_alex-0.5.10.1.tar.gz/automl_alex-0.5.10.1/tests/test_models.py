import pytest
import sys
import pandas as pd
import numpy as np
import optuna
import sklearn
import alexautoml
from alexautoml import *
#from alexautoml.databunch import *
#from alexautoml.models import *
#from alexautoml.models.sklearn_models import *

# Data
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

RANDOM_SEED = 42

@pytest.fixture
def get_data():
    data = load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(pd.DataFrame(data.data), 
                                                    pd.DataFrame(data.target), 
                                                    test_size=0.10, 
                                                    random_state=42,)
    data = DataBunch(X_train=X_train, 
                    y_train=y_train,
                    X_test=X_test,
                    y_test=y_test,
                    cat_encoder='JamesSteinEncoder',
                    random_state=RANDOM_SEED)
    return(data)

### Test Models #####################################################

def test_predict_default_model(get_data):
    data = get_data
    for model_name in all_models.keys():
        test_model = all_models[model_name](databunch=data, 
                                            cv=0, 
                                            metric='auc', 
                                            random_state=RANDOM_SEED)
        test_model.fit(data.X_train, data.y_train, data.X_test, data.y_test,)
        if test_model.is_possible_predict_proba():
            pred_proba = test_model.predict_proba(data.X_test)
        else: pred_proba = test_model.predict(data.X_test)
        assert len(pred_proba) == 57
        score = sklearn.metrics.roc_auc_score(data.y_test, pred_proba)
        if model_name == 'BernoulliNB':
            assert 0.8 < score <= 1
        else: assert 0.9 < score <= 1
        pred_proba = test_model.predict(data.X_test)
        score = sklearn.metrics.accuracy_score(data.y_test, pred_proba)
        assert 0.9 < score <= 1



def test_model_score(get_data):
    data = get_data
    for model_name in all_models.keys():
        test_model = all_models[model_name](databunch=data,
                                            metric='auc', 
                                            random_state=RANDOM_SEED)
        test_model.fit(data.X_train, data.y_train, data.X_test, data.y_test,)
        if test_model.is_possible_predict_proba():
            pred_proba = test_model.predict_proba(data.X_test)
        else: pred_proba = test_model.predict(data.X_test)
        # auc
        score = test_model.model_score()
        score2 = round(sklearn.metrics.roc_auc_score(data.y_test, pred_proba),4)
        assert 0.9 < score <= 1
        assert 0.9 < score2 <= 1
        # accuracy
        test_model = all_models[model_name](databunch=data, 
                                            metric='accuracy', 
                                            random_state=RANDOM_SEED)
        test_model.fit(data.X_train, data.y_train, data.X_test, data.y_test,)
        if test_model.is_possible_predict_proba():
            pred_proba = np.round(test_model.predict_proba(data.X_test),0)
        else: pred_proba = test_model.predict(data.X_test)
        score = test_model.model_score()
        score2 = round(sklearn.metrics.accuracy_score(data.y_test, pred_proba),4)
        assert 0.9 < score <= 1
        assert 0.9 < score2 <= 1


def test_cross_val_score(get_data):
    data = get_data
    for model_name in all_models.keys():
        test_model = all_models[model_name](databunch=data,
                                            metric='auc', 
                                            random_state=RANDOM_SEED)
        #test_model.fit(data.X_train, data.y_train, data.X_test, data.y_test,)
        score, _ = test_model.cross_val_score()
        assert score is not None
        assert score >= 0.9


def test_cross_val_predict(get_data):
    data = get_data
    for model_name in all_models.keys():
        test_model = all_models[model_name](databunch=data, random_state=RANDOM_SEED)
        stacking_feature_test, _ = test_model.cross_val_predict(print_metric=False)
        assert stacking_feature_test is not None
        score = sklearn.metrics.roc_auc_score(data.y_test, stacking_feature_test)
        assert score >= 0.95


def test_opt_default(get_data):
    data = get_data
    for model_name in all_models.keys():
        test_model = all_models[model_name](databunch=data, cv=0, random_state=RANDOM_SEED)
        s = test_model.opt(timeout=100, verbose=0,)
        assert s is not None
        assert test_model.best_score > 0.95


def test_opt_cv5(get_data):
    data = get_data
    for model_name in all_models.keys():
        test_model = all_models[model_name](databunch=data,
                                            random_state=RANDOM_SEED)
        s = test_model.opt(timeout=50, verbose=0,)
        assert s is not None
        assert test_model.best_score > 0.96
        stacking_feature_test, _ = test_model.cross_val_predict(print_metric=False)
        assert stacking_feature_test is not None
        score = sklearn.metrics.roc_auc_score(data.y_test, stacking_feature_test)
        assert score > 0.95


def test_opt_cv5_accuracy(get_data):
    data = get_data
    for model_name in all_models.keys():
        test_model = all_models[model_name](databunch=data, 
                                            metric='accuracy', 
                                            random_state=RANDOM_SEED)
        s = test_model.opt(timeout=100, verbose=0,)
        assert s is not None
        assert test_model.best_score > 0.94
        predict, _ = test_model.cross_val_predict(print_metric=False)
        assert predict is not None
        score = np.round(sklearn.metrics.accuracy_score(data.y_test, np.round(predict, 0)), 4)
        assert score > 0.9
