import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import evaluation as eval
import os
import warnings
from neural import NN_wrapper
from util import get_clean_data
from LogisticRegression import RegressionModel
from svm_model import SVMModel
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, f1_score, accuracy_score

def main():
    warnings.filterwarnings("ignore", category=FutureWarning)
    features = [
        'EMA200',
        'EMA100',
        'EMA12',
        'EMA20',
        'EMA26',
        'EMA50',
        'SMA10',
        'SMA100',
        'SMA15',
        'SMA20',
        'SMA200',
        'SMA50',
        'MACD',
        'Volume',
        'EMA200Cross',
        'EMA100Cross',
        'EMA12Cross',
        'EMA20Cross',
        'EMA26Cross',
        'EMA50Cross',
        'SMA10Cross',
        'SMA100Cross',
        'SMA15Cross',
        'SMA20Cross',
        'SMA200Cross',
        'SMA50Cross'
    ]
    label = ['Class']

    #Get Data
    df_train, df_valid, df_test = get_clean_data()
    Xtrain = df_train[features].values
    Ytrain = df_train[label].values.ravel()
    Xvalid = df_valid[features].values
    Yvalid = df_valid[label].values.ravel()
    Xtest = df_test[features].values
    Ytest = df_test[label].values.ravel()

    '''
    Training
    '''
    #Neural Network
    NN = NN_wrapper(Xtrain.shape[1])
    NN.train(Xtrain,Ytrain)

    #Logistic Regression Model
    logistic = RegressionModel(1)
    logistic_ridge = RegressionModel(2)
    logistic_lasso = RegressionModel(3)
    logistic.train(Xtrain, Ytrain)
    logistic_ridge.train(Xtrain, Ytrain)
    logistic_lasso.train(Xtrain, Ytrain)

    #SVM Model
    svm_linear = SVMModel(1)
    svm_poly = SVMModel(2)
    svm_rbf = SVMModel(3)
    svm_sigmoid = SVMModel(4)
    svm_linear.train(Xtrain, Ytrain)
    svm_poly.train(Xtrain, Ytrain)
    svm_rbf.train(Xtrain, Ytrain)
    svm_sigmoid.train(Xtrain, Ytrain)

    '''
    Prediction
    '''
    all_pred = {}
    all_pred['nn_pred'] = np.array(NN.predict(Xvalid))
    all_pred['logistic_pred'] = np.array(logistic.predict(Xvalid))
    all_pred['logistic_ridge_pred'] = np.array(logistic_ridge.predict(Xvalid))
    all_pred['logistic_lasso_pred'] = np.array(logistic_lasso.predict(Xvalid))
    all_pred['svm_linear_pred'] = np.array(svm_linear.predict(Xvalid))
    all_pred['svm_poly_pred'] = np.array(svm_poly.predict(Xvalid))
    all_pred['svm_rbf_pred'] = np.array(svm_rbf.predict(Xvalid))
    all_pred['svm_sigmoid_pred'] = np.array(svm_sigmoid.predict(Xvalid))

    '''
    Evaluation
    '''
    for key, pred in all_pred.items():
        print('Accuracy Score of', key)
        print(eval.accuarcy(prediction = pred, true_class = Yvalid))
        print('F1 Score of', key)
        print(f1_score(Yvalid, pred, average='micro'))
        print('='*50)

    '''
    Portfolio Generation
    '''
    price = df_valid['Price'].values
    for key, pred in all_pred.items():
        portfolio = eval.portfolio_generator(principal = 10000.,prediction = pred, true_price = price,threshold = [0.5,0.5] ,leverage = 1 ,short = True)
        abs_profit, annual_prof, sharpe = profit_eval(portfolio)
        print('Annual Profit for', key)
        print(annual_prof)
        print('*'*50)

if __name__ == "__main__":
    main()
