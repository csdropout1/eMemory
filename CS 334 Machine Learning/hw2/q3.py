import argparse
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV

def remove_data(x, y, percent, xx, yy):
    m,n = x.shape
    percent = percent*m
    list_of_rows = np.random.randint(0, m, int(percent))
    x = x[~x.index.isin(list_of_rows)]
    y = y[~y.index.isin(list_of_rows)]
    yy = yy[~yy.index.isin(list_of_rows)]
    xx = xx[~xx.index.isin(list_of_rows)]
    return x, y, xx, yy

def main():
    # set up the program to take in arguments from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("--xTrain",
                        default="q4xTrain.csv",
                        help="filename for features of the training data")
    parser.add_argument("--yTrain",
                        default="q4yTrain.csv",
                        help="filename for labels associated with training data")
    parser.add_argument("--xTest",
                        default="q4xTest.csv",
                        help="filename for features of the test data")
    parser.add_argument("--yTest",
                        default="q4yTest.csv",
                        help="filename for labels associated with the test data")
    args = parser.parse_args()
    # load the train and test data
    xTrain = pd.read_csv(args.xTrain).to_numpy()
    yTrain = pd.read_csv(args.yTrain).to_numpy().flatten()
    xTest = pd.read_csv(args.xTest).to_numpy()
    yTest = pd.read_csv(args.yTest).to_numpy().flatten()
    yTrain2 = pd.read_csv(args.yTrain)

    #### Part A
    '''
    param_grid = {
    'criterion': ['gini', 'entropy'],
    'max_depth': [None, 10, 20, 30, 40, 50],
    'min_samples_leaf': [x for x in range(1,20)]
    }
    param_grid2 = {
    'n_neighbors': [x for x in range(5,30)],  
    'p': [1, 2]
    }
    
    m1 = DecisionTreeClassifier()
    m2 = KNeighborsClassifier()

    bmls = []
    bmd = []
    bcri = []
    bk = []
    bp = []
    best_mls = []
    best_md = []
    best_cri = []
    best_k = []
    best_p = []
    cv_values = [2, 5, 10, 15, 20]
    for x in range(10):
        print(x)
        for i in cv_values:
            grid_search = GridSearchCV(m1, param_grid, scoring='roc_auc', cv=i)
            grid_search2 = GridSearchCV(m2, param_grid2, scoring='roc_auc', cv=i)
            grid_search.fit(xTrain, yTrain)
            grid_search2.fit(xTrain, yTrain)
            best_params = grid_search.best_params_
            best_params2 = grid_search2.best_params_

            best_mls.append(best_params['min_samples_leaf'])
            best_md.append(best_params['max_depth'])
            best_cri.append(best_params['criterion'])

            best_k.append(best_params2['n_neighbors'])
            best_p.append(best_params2['p'])
        bmls.append(max(best_mls, key=best_mls.count))
        bmd.append(max(best_md, key=best_md.count))
        bcri.append(max(best_cri, key=best_cri.count))
        bk.append(max(best_k, key=best_k.count))
        bp.append(max(best_p, key=best_p.count))
    print('minimum leaf sample: ',max(bmls, key=bmls.count))
    print('max depth: ',max(bmd, key=bmd.count))
    print('criterion: ',max(bcri, key=bcri.count))
    print('k: ',max(bk, key=bk.count))
    print('p: ',max(bp, key=bp.count))
    '''
    '''
    minimum leaf sample:  18
    max depth:  10
    criterion:  entropy
    k:  28
    p:  1
    '''
    ##### Part B
    #'''
    knn = KNeighborsClassifier(n_neighbors = 28, p = 1)
    x = pd.read_csv(args.xTrain)
    y = pd.read_csv(args.yTrain)
    test_data_y = pd.read_csv(args.yTest)
    test_data_x = pd.read_csv(args.xTest)
    knn.fit(x, y['label'])
    yHatTest = knn.predict(test_data_x)
    acc_knn = accuracy_score(yHatTest, test_data_y['label'])
    fpr, tpr, thresholds = metrics.roc_curve(test_data_y['label'],
                                            yHatTest)
    auc_knn = metrics.auc(fpr, tpr)
    print(acc_knn, auc_knn)
    percents = [0.05, 0.1, 0.2]
    accuracy_scores = []
    auc_scores = []
    for i in percents:
        temp_x, temp_y, xx, yy = remove_data(x, y, i, test_data_x, test_data_y)
        temp_knn = KNeighborsClassifier(n_neighbors = 28, p = 1)
        temp_knn.fit(temp_x, temp_y['label'])
        yHat = temp_knn.predict(xx)
        accuracy_scores.append(accuracy_score(yHat, yy['label']))
        fpr, tpr, thresholds = metrics.roc_curve(yy['label'],
                                                yHat)
        auc = metrics.auc(fpr, tpr)
        auc_scores.append(auc)
    print('Accuracy Scores: ', accuracy_scores) 
    print('AUC Scores: ', auc_scores)
    #'''
    '''
    Accuracy Scores:  [0.8630434782608696, 0.8674418604651163, 0.86]
    AUC Scores:  [0.5133541241853584, 0.49733333333333335, 0.5074750830564784]
    '''
    #### Part C
    #'''
    xTrain = pd.DataFrame(xTrain)
    yTrain = pd.DataFrame(yTrain)
    xTest = pd.DataFrame(xTest)
    yTest = pd.DataFrame(yTest)
    dtc = DecisionTreeClassifier(criterion='entropy', max_depth= 10, min_samples_leaf=18)
    
    dtc.fit(xTrain, yTrain)
    yHatTest = dtc.predict(xTest)
    acc_dtc = accuracy_score(yHatTest, yTest)
    fpr, tpr, thresholds = metrics.roc_curve(yTest,
                                            yHatTest)
    auc_dtc = metrics.auc(fpr, tpr)
    percents = [0.05, 0.1, 0.2]

    print(acc_dtc, auc_dtc)
    accuracy_scores1 = []
    auc_scores1 = []

    for i in percents:
        temp_x, temp_y, xx, yy = remove_data(xTrain, yTrain, i, xTest, yTest)
        temp_dtc = DecisionTreeClassifier(criterion='entropy', max_depth= 10, min_samples_leaf=18)
        temp_dtc.fit(temp_x, temp_y)
        yHat = temp_dtc.predict(xx)
        accuracy_scores1.append(accuracy_score(yHat, yy))
        fpr, tpr, thresholds = metrics.roc_curve(yy,
                                                 yHat)
        auc = metrics.auc(fpr, tpr)
        auc_scores1.append(auc)
    print('Accuracy Scores: ', accuracy_scores1) 
    print('AUC Scores: ', auc_scores1)
    #'''
    '''
    Accuracy Scores:  [0.888646288209607, 0.8870967741935484, 0.8740554156171285]
    AUC Scores:  [0.7247474747474748, 0.7204293785310735, 0.6598883572567783]
    '''
    print('\n')
    perfDF = pd.DataFrame([['Knn All Data: ', auc_knn, acc_knn],
                           ['    Knn - 5%: ', auc_scores[0], accuracy_scores[0]],
                           ['   Knn - 10%: ', auc_scores[1], accuracy_scores[1]],
                           ['   Knn - 20%: ', auc_scores[2], accuracy_scores[2]],
                           ['DTC All Data: ', auc_dtc, acc_dtc],
                           ['    DTC - 5%: ', auc_scores1[0], accuracy_scores1[0]],
                           ['   DTC - 10%: ', auc_scores1[1], accuracy_scores1[1]],
                           ['   DTC - 20%: ', auc_scores1[2], accuracy_scores1[2]]],
                           columns=['Model', 'Val AUC', 'Accuracy'])
    print(perfDF)
    print('\n')
    
if __name__ == "__main__":
    main()
