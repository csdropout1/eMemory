import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


def standard_scale(xTrain, xTest):
    """
    Preprocess the training data to have zero mean and unit variance.
    The same transformation should be used on the test data. For example,
    if the mean and std deviation of feature 1 is 2 and 1.5, then each
    value of feature 1 in the test set is standardized using (x-2)/1.5.

    Parameters
    ----------
    xTrain : nd-array with shape n x d
        Training data 
    xTest : nd-array with shape m x d
        Test data 

    Returns
    -------
    xTrain : nd-array with shape n x d
        Transformed training data with mean 0 and unit variance 
    xTest : nd-array with shape m x d
        Transformed test data using same process as training.
    """
    # TODO FILL IN
    xTrain = pd.DataFrame(xTrain)
    xTest = pd.DataFrame(xTest)
    for col in xTrain:
        m = np.mean(xTrain[col])
        std = np.std(xTrain[col])
        for v in range(len(xTrain[col])):
            xTrain[col][v] = (xTrain[col][v]-m)/std
    
    for col in xTest:
        m = np.mean(xTest[col])
        std = np.std(xTest[col])
        for v in range(len(xTest[col])):
            xTest[col][v] = (xTest[col][v]-m)/std

    return xTrain, xTest


def minmax_range(xTrain, xTest):
    """
    Preprocess the data to have minimum value of 0 and maximum
    value of 1.T he same transformation should be used on the test data.
    For example, if the minimum and maximum of feature 1 is 0.5 and 2, then
    then feature 1 of test data is calculated as:
    (1 / (2 - 0.5)) * x - 0.5 * (1 / (2 - 0.5))

    Parameters
    ----------
    xTrain : nd-array with shape n x d
        Training data 
    xTest : nd-array with shape m x d
        Test data 

    Returns
    -------
    xTrain : nd-array with shape n x d
        Transformed training data with min 0 and max 1.
    xTest : nd-array with shape m x d
        Transformed test data using same process as training.
    """
    xTrain = pd.DataFrame(xTrain)
    xTest = pd.DataFrame(xTest)
    # TODO FILL IN
    for col in xTrain:
        m1 = np.max(xTrain[col])
        m2 = np.min(xTrain[col])
        r = m1-m2
        for v in range(len(xTrain[col])):
            xTrain[col][v] = (1/r)* xTrain[col][v] - m2*(1/r)
    
    for col in xTest:
        m1 = np.max(xTest[col])
        m2 = np.min(xTest[col])
        r = m1-m2
        for v in range(len(xTest[col])):
            xTest[col][v] = (1/r)* xTest[col][v] - m2*(1/r)
  
    return xTrain, xTest


def add_irr_feature(xTrain, xTest):
    """
    Add 2 features using Gaussian distribution with 0 mean,
    standard deviation of 1.

    Parameters
    ----------
    xTrain : nd-array with shape n x d
        Training data 
    xTest : nd-array with shape m x d
        Test data 

    Returns
    -------
    xTrain : nd-array with shape n x (d+2)
        Training data with 2 new noisy Gaussian features
    xTest : nd-array with shape m x (d+2)
        Test data with 2 new noisy Gaussian features
    """
    xTrain = pd.DataFrame(xTrain)
    xTest = pd.DataFrame(xTest)
    # TODO FILL IN
    n = len(xTrain)
    m = len(xTest)
    for i in range(2):
        string = 'irr_feature_'+str(i+1)
        q = np.random.normal(0, 1, n)
        r = np.random.normal(0, 1, m)
        xTrain[string] = q
        xTest[string] = r

    return xTrain, xTest


def knn_train_test(k, xTrain, yTrain, xTest, yTest):
    """
    Given a specified k, train the knn model and predict
    the labels of the test data. Returns the accuracy of
    the resulting model.

    Parameters
    ----------
    k : int
        The number of neighbors
    xTrain : nd-array with shape n x d
        Training data 
    yTrain : 1d array with shape n
        Array of labels associated with training data.
    xTest : nd-array with shape m x d
        Test data 
    yTest : 1d array with shape m
        Array of labels associated with test data.

    Returns
    -------
    acc : float
        The accuracy of the trained knn model on the test data
    """
    knn = KNeighborsClassifier(n_neighbors=k, metric='minkowski', p =2)
    knn.fit(xTrain, yTrain['label']) 
    # predict the test dataset
    yHatTest = knn.predict(xTest)
    return accuracy_score(yHatTest, yTest['label'])
    

def main():
    # set up the program to take in arguments from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("k",
                        type=int,
                        help="the number of neighbors")
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
    xTrain = pd.read_csv(args.xTrain)
    yTrain = pd.read_csv(args.yTrain)
    xTest = pd.read_csv(args.xTest)
    yTest = pd.read_csv(args.yTest)
    
    # no preprocessing
    acc1 = knn_train_test(args.k, xTrain, yTrain, xTest, yTest)
    print("Test Acc (no-preprocessing):", acc1)
    # preprocess the data using standardization scaling
    xTrainStd, xTestStd = standard_scale(xTrain, xTest)
    
    acc2 = knn_train_test(args.k, xTrainStd, yTrain, xTestStd, yTest)
    print("Test Acc (standard scale):", acc2)
    # preprocess the data using min max scaling
    xTrainMM, xTestMM = minmax_range(xTrain, xTest)
    
    acc3 = knn_train_test(args.k, xTrainMM, yTrain, xTestMM, yTest)
    print("Test Acc (min max scale):", acc3)
    # add irrelevant features
    xTrainIrr, yTrainIrr = add_irr_feature(xTrain, xTest)
    acc4 = knn_train_test(args.k, xTrainIrr, yTrain, yTrainIrr, yTest)
    print("Test Acc (with irrelevant feature):", acc4)
    
#### TESTING 
    # no_pre = []
    # stand = []
    # mm_scale = []
    # irr = []
    # for i in range(args.k):
    #     i += 1
    #     acc1 = knn_train_test(i, xTrain, yTrain, xTest, yTest)
    #     no_pre.append(acc1)
    #     # preprocess the data using standardization scaling
    #     xTrainStd, xTestStd = standard_scale(xTrain, xTest)
        
    #     acc2 = knn_train_test(i, xTrainStd, yTrain, xTestStd, yTest)
    #     stand.append(acc2)
    #     # preprocess the data using min max scaling
    #     xTrainMM, xTestMM = minmax_range(xTrain, xTest)
        
    #     acc3 = knn_train_test(i, xTrainMM, yTrain, xTestMM, yTest)
    #     mm_scale.append(acc3)
    #     # add irrelevant features
    #     xTrainIrr, yTrainIrr = add_irr_feature(xTrain, xTest)
    #     acc4 = knn_train_test(i, xTrainIrr, yTrain, yTrainIrr, yTest)
    #     irr.append(acc4)
    	
    # d = pd.DataFrame({'No Preprocessing': no_pre, 'Standard Scale': stand, 'MinMax Scale': mm_scale, 'Added Irr Features': irr})
    # d.plot.line()
    # plt.show()

if __name__ == "__main__":
    main()
