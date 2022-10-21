import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import mean_absolute_error
import joblib
import pandas as pd 
import numpy as np

from functions.config import seed
from functions.config import eval_metric
from functions.config import learning_rate
from functions.config import n_estimators
from functions.config import max_depth
from functions.config import colsample_bytree
from functions.config import subsample
from functions.config import date_string

def train_regressor(X_train, 
                    y_train,
                    seed = seed, 
                    eval_metric = eval_metric,
                    learning_rate = learning_rate, 
                    n_estimators = n_estimators, 
                    max_depth = max_depth, 
                    colsample_bytree = colsample_bytree,
                    # subsample = subsample, 
                    date_string = date_string
                   ):
    
    regressor = xgb.XGBRegressor(random_state = seed,
                             eval_metric = eval_metric, 
                             learning_rate = learning_rate,
                             n_estimators = n_estimators, 
                             max_depth = max_depth, 
                             colsample_bytree = colsample_bytree,
                             # subsample = subsample
                            )
    
    regressor.fit(X_train, y_train)
    
    # Save model
    joblib.dump(regressor, str('data/model/xgboost_' + date_string + '.csv')) 
    
    return regressor

def eval_regressor(X_train, 
                   y_train, 
                   X_test, 
                   y_test, 
                   regressor):
    
    # Train Set Statistics
    ypred_train = regressor.predict(X_train)
    mse = mean_squared_error(y_train, ypred_train)
    mape = mean_absolute_percentage_error(y_train, ypred_train)
    mae = mean_absolute_error(y_train, ypred_train)

    print('Train Set Statistics: ')
    print('MSE: ', mse)
    print('RMSE: ', np.sqrt(mse))
    print('MAPE: ', mape) 
    print('MAE: ', mae) 
    
    # Test Set Statistics
    ypred = regressor.predict(X_test)
    mse = mean_squared_error(y_test, ypred)
    mape = mean_absolute_percentage_error(y_test, ypred)
    mae = mean_absolute_error(y_test, ypred)

    print('Test Set Statistics: ')
    print('MSE: ', mse)
    print('RMSE: ', np.sqrt(mse))
    print('MAPE: ', mape) 
    print('MAE: ', mae) 
    
    return y_train, ypred_train, y_test, ypred