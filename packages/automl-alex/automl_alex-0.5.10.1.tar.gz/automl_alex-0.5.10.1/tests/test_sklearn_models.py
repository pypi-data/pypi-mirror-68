import pytest
import sys
import pandas as pd
import numpy as np
import optuna
import sklearn
#sys.path.append("..")
import alexautoml
from alexautoml.databunch import DataBunch
from alexautoml.models.sklearn_models import LogRegClassifier


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
                    random_state=RANDOM_SEED)
    return(data)


######### LogRegClassifier #####################################################
@pytest.fixture
def get_model_param():
    return({'max_iter': 2000,
            'n_jobs': -1,
            'verbose': 0,
            'random_state': 42,
            'solver': 'saga',
            'C': 0.3584657285442726,
            'tol': 0.011587790083453446,
            'class_weight': None,
            'penalty': 'l1'})

@pytest.fixture
def get_wrapper_params():
    return({
            'need_norm_data':True,
            'norm_data':True,
            'scaler_name':'RobustScaler',
            })
    

### Test LogRegClassifier #####################################################

def test_predict_default_model(get_data):
    data = get_data
    test_model = LogRegClassifier(databunch=data, random_state=RANDOM_SEED)
    test_model.fit(test_model.X_train, test_model.y_train, test_model.X_test, test_model.y_test,)
    pred_proba = test_model.predict_proba(test_model.X_test)
    assert len(pred_proba) == 57
    score = sklearn.metrics.roc_auc_score(data.y_test, pred_proba)
    assert 0.98 < score < 0.999
    pred_proba = test_model.predict(test_model.X_test)
    score = sklearn.metrics.accuracy_score(data.y_test, pred_proba)
    assert 0.95 < score < 0.999
    
    
def test_predict_config_model(get_data, get_model_param, get_wrapper_params):
    data = get_data
    test_model = LogRegClassifier(databunch=data,
                                    model_param = get_model_param,
                                    wrapper_params = get_wrapper_params,
                                    random_state=RANDOM_SEED)
    test_model.fit(test_model.X_train, test_model.y_train, test_model.X_test, test_model.y_test,)
    pred_proba = test_model.predict_proba(test_model.X_test)
    assert len(pred_proba) == 57
    score = sklearn.metrics.roc_auc_score(data.y_test, pred_proba)
    assert 0.93 < score < 0.999
    pred_proba = test_model.predict(test_model.X_test)
    score = sklearn.metrics.accuracy_score(data.y_test, pred_proba)
    assert 0.93 < score < 0.99


def test_model_score(get_data):
    data = get_data
    test_model = LogRegClassifier(databunch=data, metric='auc', random_state=RANDOM_SEED)
    score = test_model.model_score(metric='auc')
    assert score >= 0.97
    score = test_model.model_score(metric='accuracy')
    assert score >= 0.96


def test_cross_val_score(get_data):
    data = get_data
    test_model = LogRegClassifier(databunch=data, metric='auc', random_state=RANDOM_SEED)
    score, _ = test_model.cross_val_score()
    assert score is not None
    assert 0.98 < score < 0.999
    test_model = LogRegClassifier(databunch=data, metric='accuracy', random_state=RANDOM_SEED)
    score, _ = test_model.cross_val_score()
    assert 0.95 < score < 0.99


def test_cross_val_predict(get_data):
    data = get_data
    test_model = LogRegClassifier(databunch=data, random_state=RANDOM_SEED)
    stacking_feature_test, _ = test_model.cross_val_predict(print_metric=False)
    assert stacking_feature_test is not None
    score = sklearn.metrics.roc_auc_score(data.y_test, stacking_feature_test)
    assert score >= 0.98


def test_opt_default(get_data):
    data = get_data
    test_model = LogRegClassifier(databunch=data, cv=0, random_state=RANDOM_SEED)
    s = test_model.opt(timeout=30, verbose=0,)
    assert s is not None
    assert 0.95 < test_model.best_score < 0.999


def test_opt_cv5(get_data):
    data = get_data
    test_model = LogRegClassifier(databunch=data, cv=5, random_state=RANDOM_SEED)
    s = test_model.opt(timeout=50, verbose=0,)
    assert s is not None
    assert 0.98 < test_model.best_score < 0.999
    stacking_feature_test, _ = test_model.cross_val_predict(print_metric=False)
    assert stacking_feature_test is not None
    score = np.round(sklearn.metrics.roc_auc_score(data.y_test, stacking_feature_test),4)
    assert 0.98 < score < 0.999


def test_opt_cv5_accuracy(get_data):
    data = get_data
    test_model = LogRegClassifier(databunch=data, cv=5, metric='accuracy', random_state=RANDOM_SEED)
    s = test_model.opt(timeout=30, verbose=0,)
    assert s is not None
    assert 0.97 < test_model.best_score < 0.999
    stacking_feature_test, _ = test_model.cross_val_predict(print_metric=False)
    assert stacking_feature_test is not None
    score = sklearn.metrics.accuracy_score(data.y_test, np.round(stacking_feature_test,0))
    assert 0.96 < score < 0.99