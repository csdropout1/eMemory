import argparse
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import time
 
def holdout(model, xFeat, y, testSize):
    """
    Split xFeat into random train and test based on the testSize and
    return the model performance on the training and test set. 

    Parameters
    ----------
    model : sktree.DecisionTreeClassifier
        Decision tree model
    xFeat : numpy.nd-array with shape n x d
        Features of the dataset 
    y : numpy.1d-array with shape n 
        Labels of the dataset
    testSize : float
        Portion of the dataset to serve as a holdout. 

    Returns
    -------
    trainAuc : float
        Average AUC of the model on the training dataset
    testAuc : float
        Average AUC of the model on the validation dataset
    timeElapsed: float
        Time it took to run this function
    """
    trainAuc = 0
    testAuc = 0
    timeElapsed = 0
    # TODO fill int
    df = pd.DataFrame(xFeat)
    y = pd.DataFrame(y)
    m,n = df.shape
    start = time.time()
    testSize = int(testSize*m)
    list_of_rows = np.random.randint(0, m, testSize)
    
    xTest = df.loc[list_of_rows]
    yTest = y.loc[list_of_rows]
    xTrain = df[~df.index.isin(list_of_rows)]
    yTrain = y[~y.index.isin(list_of_rows)]

    model.fit(xTrain, yTrain)

    yHatTrain = model.predict_proba(xTrain)
    yHatTest = model.predict_proba(xTest)
    fpr, tpr, thresholds = metrics.roc_curve(yTrain,
                                             yHatTrain[:, 1])
    trainAuc = metrics.auc(fpr, tpr)

    fpr, tpr, thresholds = metrics.roc_curve(yTest,
                                             yHatTest[:, 1])
    testAuc = metrics.auc(fpr, tpr)
    timeElapsed = time.time() - start
    return trainAuc, testAuc, timeElapsed

    #trainAuc, testAuc = accuracy_score(yTrain, model.predict(xTrain)), accuracy_score(yTest, model.predict(xTest))

    #timeElapsed = time.time() - start
    #return trainAuc, testAuc, timeElapsed


def kfold_cv(model, xFeat, y, k):
    """
    Split xFeat into k different groups, and then use each of the
    k-folds as a validation set, with the model fitting on the remaining
    k-1 folds. Return the model performance on the training and
    validation (test) set. 


    Parameters
    ----------
    model : sktree.DecisionTreeClassifier
        Decision tree model
    xFeat : numpy.nd-array with shape n x d
        Features of the dataset 
    y : numpy.1d-array with shape n
        Labels of the dataset
    k : int
        Number of folds or groups (approximately equal size)

    Returns
    -------
    trainAuc : float
        Average AUC of the model on the training dataset
    testAuc : float
        Average AUC of the model on the validation dataset
    timeElapsed: float
        Time it took to run this function
    """
    trainAuc = 0
    testAuc = 0
    timeElapsed = 0
    # TODO FILL IN
    df = pd.DataFrame(xFeat)
    y = pd.DataFrame(y)
    m,n = df.shape
    start = time.time()

    list_of_row_group = []
    all_rows = list(range(0, m))
    np.random.shuffle(all_rows)
    group_size = int(m/k)
    i = 0
    while len(list_of_row_group) <k:
        list_of_row_group.append(all_rows[i: i+group_size])
        i += group_size

    for item in list_of_row_group:
        xTest = df.loc[item]
        yTest = y.loc[item]
        xTrain = df[~df.index.isin(item)]
        yTrain = y[~y.index.isin(item)]

        model.fit(xTrain, yTrain)
        yHatTrain = model.predict_proba(xTrain)
        yHatTest = model.predict_proba(xTest)
        fpr, tpr, thresholds = metrics.roc_curve(yTrain,
                                               yHatTrain[:, 1])
        a = metrics.auc(fpr, tpr)

        fpr, tpr, thresholds = metrics.roc_curve(yTest,
                                               yHatTest[:, 1])
        b = metrics.auc(fpr, tpr)
        trainAuc += a
        testAuc += b

    trainAuc = trainAuc/k
    testAuc = testAuc/k
    timeElapsed = time.time() - start
    return trainAuc, testAuc, timeElapsed

def mc_cv(model, xFeat, y, testSize, s):
    """
    Evaluate the model using s samples from the
    Monte Carlo cross validation approach where
    for each sample you split xFeat into
    random train and test based on the testSize.
    Returns the model performance on the training and
    test datasets.

    Parameters
    ----------
    model : sktree.DecisionTreeClassifier
        Decision tree model
    xFeat : numpy.nd-array with shape n x d
        Features of the dataset 
    y : numpy.1d-array with shape n
        Labels of the dataset
    testSize : float
        Portion of the dataset to serve as a holdout. 

    Returns
    -------
    trainAuc : float
        Average AUC of the model on the training dataset
    testAuc : float
        Average AUC of the model on the validation dataset
    timeElapsed: float
        Time it took to run this function
    """
    trainAuc = 0
    testAuc = 0
    timeElapsed = 0
    # TODO FILL IN
    df = pd.DataFrame(xFeat)
    y = pd.DataFrame(y)
    m,n = df.shape
    start = time.time()
    for q in range(s):
        t = int(testSize*m)
        list_of_rows = np.random.randint(0, m, t)

        xTest = df.loc[list_of_rows]
        yTest = y.loc[list_of_rows]
        xTrain = df[~df.index.isin(list_of_rows)]
        yTrain = y[~y.index.isin(list_of_rows)]
        
        model.fit(xTrain, yTrain)
        yHatTrain = model.predict_proba(xTrain)
        yHatTest = model.predict_proba(xTest)
        fpr, tpr, thresholds = metrics.roc_curve(yTrain,
                                               yHatTrain[:, 1])
        a = metrics.auc(fpr, tpr)

        fpr, tpr, thresholds = metrics.roc_curve(yTest,
                                               yHatTest[:, 1])
        b = metrics.auc(fpr, tpr)
        trainAuc += a
        testAuc += b
    
    trainAuc = trainAuc/s
    testAuc = testAuc/s
    timeElapsed = time.time() - start
    return trainAuc, testAuc, timeElapsed


def sktree_train_test(model, xTrain, yTrain, xTest, yTest):
    """
    Given a sklearn tree model, train the model using
    the training dataset, and evaluate the model on the
    test dataset.

    Parameters
    ----------
    model : DecisionTreeClassifier object
        An instance of the decision tree classifier 
    xTrain : numpy.nd-array with shape nxd
        Training data
    yTrain : numpy.1d array with shape n
        Array of labels associated with training data
    xTest : numpy.nd-array with shape mxd
        Test data
    yTest : numpy.1d array with shape m
        Array of labels associated with test data.

    Returns
    -------
    trainAUC : float
        The AUC of the model evaluated on the training data.
    testAuc : float
        The AUC of the model evaluated on the test data.
    """
    # fit the data to the training dataset
    model.fit(xTrain, yTrain)
    # predict training and testing probabilties
    yHatTrain = model.predict_proba(xTrain)
    yHatTest = model.predict_proba(xTest)
    # calculate auc for training
    fpr, tpr, thresholds = metrics.roc_curve(yTrain,
                                             yHatTrain[:, 1])
    trainAuc = metrics.auc(fpr, tpr)
    # calculate auc for test dataset
    fpr, tpr, thresholds = metrics.roc_curve(yTest,
                                             yHatTest[:, 1])
    testAuc = metrics.auc(fpr, tpr)
    return trainAuc, testAuc


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
    # create the decision tree classifier
    
    dtClass = DecisionTreeClassifier(max_depth=15,
                                     min_samples_leaf=10)
    #'''
    # use the holdout set with a validation size of 30 of training
    aucTrain1, aucVal1, time1 = holdout(dtClass, xTrain, yTrain, 0.30)
    # use 2-fold validation
    aucTrain2, aucVal2, time2 = kfold_cv(dtClass, xTrain, yTrain, 2)
    # use 5-fold validation
    aucTrain3, aucVal3, time3 = kfold_cv(dtClass, xTrain, yTrain, 5)
    # use 10-fold validation
    aucTrain4, aucVal4, time4 = kfold_cv(dtClass, xTrain, yTrain, 10)
    # use MCCV with 5 samples
    aucTrain5, aucVal5, time5 = mc_cv(dtClass, xTrain, yTrain, 0.30, 5)
    # use MCCV with 10 samples
    aucTrain6, aucVal6, time6 = mc_cv(dtClass, xTrain, yTrain, 0.30, 10)
    # train it using all the data and assess the true value
    trainAuc, testAuc = sktree_train_test(dtClass, xTrain, yTrain, xTest, yTest)
    perfDF = pd.DataFrame([['Holdout', aucTrain1, aucVal1, time1],
                           ['2-fold', aucTrain2, aucVal2, time2],
                           ['5-fold', aucTrain3, aucVal3, time3],
                           ['10-fold', aucTrain4, aucVal4, time4],
                           ['MCCV w/ 5', aucTrain5, aucVal5, time5],
                           ['MCCV w/ 10', aucTrain6, aucVal6, time6],
                           ['True Test', trainAuc, testAuc, 0]],
                           columns=['Strategy', 'TrainAUC', 'ValAUC', 'Time'])
    print(perfDF)
    #'''
    '''
    aucTrain1, aucTrain2, aucTrain3, aucTrain4, aucTrain5, aucTrain6, aucTrain7 = 0, 0, 0, 0, 0, 0, 0
    aucVal1, aucVal2, aucVal3, aucVal4, aucVal5, aucVal6, aucVal7 = 0, 0, 0, 0, 0, 0, 0
    time1, time2, time3, time4, time5, time6 = 0, 0, 0, 0, 0, 0
    
    for a in range(10):
        a1, b1, c1 = holdout(dtClass, xTrain, yTrain, 0.30)
        # use 2-fold validation
        a2, b2, c2 = kfold_cv(dtClass, xTrain, yTrain, 2)
        # use 5-fold validation
        a3, b3, c3 = kfold_cv(dtClass, xTrain, yTrain, 5)
        # use 10-fold validation
        a4, b4, c4 = kfold_cv(dtClass, xTrain, yTrain, 10)
        # use MCCV with 5 samples
        a5, b5, c5 = mc_cv(dtClass, xTrain, yTrain, 0.30, 5)
        # use MCCV with 10 samples
        a6, b6, c6 = mc_cv(dtClass, xTrain, yTrain, 0.30, 10)
        # train it using all the data and assess the true value
        a7, b7 = sktree_train_test(dtClass, xTrain, yTrain, xTest, yTest)
        aucTrain1 += a1
        aucTrain2 += a2
        aucTrain3 += a3
        aucTrain4 += a4
        aucTrain5 += a5
        aucTrain6 += a6
        aucTrain7 += a7
        aucVal1 += b1
        aucVal2 += b2
        aucVal3 += b3
        aucVal4 += b4
        aucVal5 += b5
        aucVal6 += b6
        aucVal7 += b7
        time1 += c1
        time2 += c2
        time3 += c3
        time4 += c4
        time5 += c5
        time6 += c6
    aucTrain1 /= 10
    aucTrain2 /= 10
    aucTrain3 /= 10
    aucTrain4 /= 10 
    aucTrain5 /= 10
    aucTrain6 /= 10
    aucTrain7 /= 10
    aucVal1 /= 10
    aucVal2 /= 10
    aucVal3 /= 10
    aucVal4 /= 10
    aucVal5 /= 10
    aucVal6 /= 10
    aucVal7 /= 10
    time1 /= 10
    time2 /= 10
    time3 /= 10
    time4 /= 10
    time5 /= 10
    time6 /= 10
    perfDF = pd.DataFrame([['Holdout', aucTrain1, aucVal1, time1],
                        ['2-fold', aucTrain2, aucVal2, time2],
                        ['5-fold', aucTrain3, aucVal3, time3],
                        ['10-fold', aucTrain4, aucVal4, time4],
                        ['MCCV w/ 5', aucTrain5, aucVal5, time5],
                        ['MCCV w/ 10', aucTrain6, aucVal6, time6],
                        ['True Test', aucTrain7, aucVal7, 0]],
                        columns=['Strategy', 'TrainAUC', 'ValAUC', 'Time'])
    print(perfDF)

    '''

if __name__ == "__main__":
    main()
