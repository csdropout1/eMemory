import argparse
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt


def calculate_split_score(y, criterion):
    """
    Given a numpy array of labels associated with a node, y, 
    calculate the score based on the crieterion specified.

    Parameters
    ----------
    y : numpy.1d array with shape n
        Array of labels associated with a node
    criterion : String
            The function to measure the quality of a split.
            Supported criteria are "gini" for the Gini impurity
            and "entropy" for the information gain.
    Returns
    -------
    score : float
        The gini or entropy associated with a node
    """

    if len(y) == 0:
        return 0

    uniques, counts = np.unique(y, return_counts=True)
    p = counts / len(y)
    if criterion == 'gini':
        return float(1 - np.sum(p*p))
    if criterion == 'entropy':
        return float(-1* np.sum(p*np.log2(p)))
    return ValueError('Value must be \'gini\' or \'entropy\' only')

class DecisionTree(object):
    maxDepth = 0       # maximum depth of the decision tree
    minLeafSample = 0  # minimum number of samples in a leaf
    criterion = None   # splitting criterion
    tree = None

    def __init__(self, criterion, maxDepth, minLeafSample):
        """
        Decision tree constructor

        Parameters
        ----------
        criterion : String
            The function to measure the quality of a split.
            Supported criteria are "gini" for the Gini impurity
            and "entropy" for the information gain.
        maxDepth : int 
            Maximum depth of the decision tree
        minLeafSample : int 
            Minimum number of samples in the decision tree
        """
        self.criterion = criterion
        self.maxDepth = maxDepth
        self.minLeafSample = minLeafSample

    def best_split(self, df, y):

        m, n = df.shape
        if m < self.minLeafSample:
            return None, None

        impurity = 1
        feature = None
        val = None

        for col in df:
            unique_values = np.unique(df[col])

            for x in unique_values:
                left_split = df[col] <= x
                right_split = df[col] > x
            
                ll = len(y[left_split])
                lr = len(y[right_split])

                if ll == 0 or lr == 0:
                    continue

                left_cri = calculate_split_score(y[left_split], self.criterion)
                right_cri = calculate_split_score(y[right_split], self.criterion)
                weighted_cri = (ll / m) * left_cri + (lr / m) * right_cri

                if weighted_cri < impurity:
                    impurity = weighted_cri
                    feature = col
                    val = x
        return feature, val

    def decision_tree(self, df, y, depth=0):
        if len(np.unique(y.iloc[:,0])) == 1:
            return y.iloc[0,0]
        if depth == self.maxDepth:
            return np.argmax(np.bincount(y.iloc[:,0]))
            
        feature, val = self.best_split(df, y)

        if feature is None:
            return np.argmax(np.bincount(y.iloc[:,0]))
        
        left_split = df[feature] <= val
        right_split = df[feature] > val

        left = self.decision_tree(df[left_split], y[left_split], depth+1)
        right = self.decision_tree(df[right_split], y[right_split], depth+1)

        return [left, right, feature, val]

    def train(self, xFeat, y):
        """
        Train the decision tree model.

        Parameters
        ----------
        xFeat : numpy.nd-array with shape n x d
            Training data 
        y : numpy.1d array with shape n
            Array of labels associated with training data.

        Returns
        -------
        self : object
        """
    
        # TODO do whatever you need
        df = pd.DataFrame(xFeat)
        y = pd.DataFrame(y)
        self.tree = self.decision_tree(df, y)

        return self

    def find_in_tree(self, node, x):
        if isinstance(node, list):
            left, right, feature, val = node[0],node[1],node[2],node[3]
            if x[feature] <= val:
                return self.find_in_tree(left, x)
            else:
                return self.find_in_tree(right, x)
        else:
            return node
    
    def predict(self, xFeat):
        """
        Given the feature set xFeat, predict 
        what class the values will have.

        Parameters
        ----------
        xFeat : numpy.nd-array with shape m x d
            The data to predict.  

        Returns
        -------
        yHat : numpy.1d array with shape m
            Predicted class label per sample
        """
        df = pd.DataFrame(xFeat)
        m,n = xFeat.shape
        yHat = np.array([0]*m) # variable to store the estimated class label
        # TODO
        for row in range(m):
            yHat[row] = self.find_in_tree(self.tree, df.loc[row])
        return yHat


def dt_train_test(dt, xTrain, yTrain, xTest, yTest):
    """
    Given a decision tree model, train the model and predict
    the labels of the test data. Returns the accuracy of
    the resulting model.

    Parameters
    ----------
    dt : DecisionTree
        The decision tree with the model parameters
    xTrain : numpy.nd-array with shape n x d
        Training data 
    yTrain : numpy.1d array with shape n
        Array of labels associated with training data.
    xTest : numpy.nd-array with shape m x d
        Test data 
    yTest : numpy.1d array with shape m
        Array of labels associated with test data.

    Returns
    -------
    acc : float
        The accuracy of the trained knn model on the test data
    """
    # train the model
    dt.train(xTrain, yTrain)
    # predict the training dataset
    yHatTrain = dt.predict(xTrain)
    trainAcc = accuracy_score(yTrain, yHatTrain)
    # predict the test dataset
    yHatTest = dt.predict(xTest)
    testAcc = accuracy_score(yTest, yHatTest)
    return trainAcc, testAcc


def main():
    """
    Main file to run from the command line.
    """
    # set up the program to take in arguments from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("md",
                        type=int,
                        help="maximum depth")
    parser.add_argument("mls",
                        type=int,
                        help="minimum leaf samples")
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
    # create an instance of the decision tree using gini
    #'''
    dt1 = DecisionTree('gini', args.md, args.mls)
    trainAcc1, testAcc1 = dt_train_test(dt1, xTrain, yTrain, xTest, yTest)
    print("GINI Criterion ---------------")
    print("Training Acc:", trainAcc1)
    print("Test Acc:", testAcc1)

    dt = DecisionTree('entropy', args.md, args.mls)
    trainAcc, testAcc = dt_train_test(dt, xTrain, yTrain, xTest, yTest)
    print("Entropy Criterion ---------------")
    print("Training Acc:", trainAcc)
    print("Test Acc:", testAcc)
    #'''
    ####### Plots
    '''
    md = args.md
    mls = args.mls

    gini_trainings = []
    gini_testings = []
    entropy_trainings = []
    entropy_testings = []

    for i in range(md):
        i += 2
        dt = DecisionTree('entropy', i, 2)
        dtc = DecisionTree('gini', i, 2)

        trainAcc, testAcc = dt_train_test(dt, xTrain, yTrain, xTest, yTest)
        trainAcc1, testAcc1 = dt_train_test(dtc, xTrain, yTrain, xTest, yTest)

        entropy_trainings.append(trainAcc)
        entropy_testings.append(testAcc)
        gini_trainings.append(trainAcc1)
        gini_testings.append(testAcc1)

    d = pd.DataFrame({'GINI Test': gini_testings, 'GINI Train': gini_trainings, 'Entropy Test': entropy_testings, 'Entropy Train': entropy_trainings})
    d.plot.line()
    
    gini_trainings = []
    gini_testings = []
    entropy_trainings = []
    entropy_testings = []

    for i in range(mls):
        i += 2
        dt = DecisionTree('entropy', 4, i)
        dtc = DecisionTree('gini', 4, i)

        trainAcc, testAcc = dt_train_test(dt, xTrain, yTrain, xTest, yTest)
        trainAcc1, testAcc1 = dt_train_test(dtc, xTrain, yTrain, xTest, yTest)

        entropy_trainings.append(trainAcc)
        entropy_testings.append(testAcc)
        gini_trainings.append(trainAcc1)
        gini_testings.append(testAcc1)

    d = pd.DataFrame({'GINI Test': gini_testings, 'GINI Train': gini_trainings, 'Entropy Test': entropy_testings, 'Entropy Train': entropy_trainings})
    d.plot.line()
    plt.show()
    '''

if __name__ == "__main__":
    main()
