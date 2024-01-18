import argparse
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV 
import matplotlib.pyplot as plt

def generate_bootstrap(xTrain, yTrain):
    """
    Helper function to generate a bootstrap sample from the data. Each
    call should generate a different random bootstrap sample!

    Parameters
    ----------
    xTrain : nd-array with shape n x d
        Training data 
    yTrain : 1d array with shape n
        Array of responses associated with training data.

    Returns
    -------
    xBoot : nd-array with shape n x d
        Bootstrap sample from xTrain
    yBoot : 1d array with shape n
        Array of responses associated with xBoot
    oobIdx : 1d array with shape k (which can be 0-(n-1))
        Array containing the out-of-bag sample indices from xTrain 
        such that using this array on xTrain will yield a matrix 
        with only the out-of-bag samples (i.e., xTrain[oobIdx, :]).
    """
    num_data = len(xTrain)

    array_index = [x for x in range(num_data)]
    all_set = set(array_index)
    array_index = np.array(array_index)
    
    array_index = np.random.choice(array_index, num_data)

    xBoot = [[0]*len(xTrain[0])]*num_data
    yBoot = [0]*num_data

    for x in range(num_data):
        xBoot[x] = xTrain[array_index[x]]
        yBoot[x] = yTrain[array_index[x]]
    
    in_bag = set(array_index)
    out_bag = all_set.difference(in_bag)
    oobIdx = list(out_bag)

    return np.array(xBoot), np.array(yBoot), np.array(oobIdx)


def generate_subfeat(xTrain, maxFeat):
    """
    Helper function to generate a subset of the features from the data. Each
    call is likely to yield different columns (assuming maxFeat is less than
    the original dimension)

    Parameters
    ----------
    xTrain : nd-array with shape n x d
        Training data 
    maxFeat : int
        Maximum number of features to consider in each tree

    Returns
    -------
    xSubfeat : nd-array with shape n x maxFeat
        Subsampled features from xTrain
    featIdx: 1d array with shape maxFeat
        Array containing the subsample indices of features from xTrain
    """
    feature_perm = np.random.permutation(len(xTrain[0]))
    featIdx = feature_perm[:maxFeat]

    xSubfeat = xTrain[:, featIdx].copy()

    return np.array(xSubfeat), np.array(featIdx)


class RandomForest(object):
    nest = 0           # number of trees
    maxFeat = 0        # maximum number of features
    maxDepth = 0       # maximum depth of the decision tree
    minLeafSample = 0  # minimum number of samples in a leaf
    criterion = None   # splitting criterion
    model = {}         # keeping track of all the models developed, where
                       # the key is the bootstrap sample. The value should be a dictionary
                       # and have 2 keys: "tree" to store the tree built
                       # "feat" to store the corresponding featIdx used in the tree

    def __init__(self, nest, maxFeat, criterion, maxDepth, minLeafSample):
        """
        Decision tree constructor

        Parameters
        ----------
        nest: int
            Number of trees to have in the forest
        maxFeat: int
            Maximum number of features to consider in each tree
        criterion : String
            The function to measure the quality of a split.
            Supported criteria are "gini" for the Gini impurity
            and "entropy" for the information gain.
        maxDepth : int 
            Maximum depth of the decision tree
        minLeafSample : int 
            Minimum number of samples in the decision tree
        """
        self.nest = nest
        self.criterion = criterion
        self.maxDepth = maxDepth
        self.minLeafSample = minLeafSample
        self.maxFeat = maxFeat

    def train(self, xFeat, y):
        """
        Train the random forest using the data

        Parameters
        ----------
        xFeat : nd-array with shape n x d
            Training data 
        y : 1d array with shape n
            Array of responses associated with training data.

        Returns
        -------
        stats : object
            Keys represent the number of trees and
            the values are the out of bag errors
        """
        oob_errors = {}

        for b in range(self.nest):
            xBoot, yBoot, oobIdx = generate_bootstrap(xFeat, y)
            xSubfeat, featIdx = generate_subfeat(xBoot, self.maxFeat)

            tree = DecisionTreeClassifier(
                criterion=self.criterion,
                max_depth=self.maxDepth,
                min_samples_leaf=self.minLeafSample
            )
            tree.fit(xSubfeat, yBoot)
            value_dic = {}
            value_dic["tree"], value_dic["feat"] = tree, featIdx
            # value_dic["oob"] = oobIdx 
            self.model[b] = value_dic

            # average ?
            if b == 0:
                s = xFeat[:, self.model[b]["feat"]].copy()
                oob_pred = tree.predict(s)
                oob_error = 1 - accuracy_score(y, oob_pred)
                oob_errors[b+1] = oob_error
            else:
                oob_error_total, oob_error_count = 0, 0
                for i in range(b):
                    # if set(oobIdx) & set(self.model[i]["oob"]):
                    #     #do nothing because sample is in training model
                    #     print("hello World")
                    # else:
                        s = xFeat[:, self.model[b]["feat"]].copy()
                        oob_pred = self.model[i]["tree"].predict(s[oobIdx])
                        oob_error = 1 - accuracy_score(y[oobIdx], oob_pred)
                        oob_error_total += oob_error
                        oob_error_count += 1
                oob_errors[b+1] = oob_error_total/oob_error_count
                        

        return oob_errors

    def predict(self, xFeat):
        """
        Given the feature set xFeat, predict 
        what class the values will have.

        Parameters
        ----------
        xFeat : nd-array with shape m x d
            The data to predict.  

        Returns
        -------
        yHat : 1d array or list with shape m
            Predicted response per sample
        """
        yHat = []
        n = len(xFeat)

        for i in range(n):
            s = xFeat[i] # sample
            class_predictions = []
            for b in range(self.nest):
                ss = s[self.model[b]["feat"]]
             
                pred = self.model[b]["tree"].predict(ss.reshape(1, -1))
                class_predictions.append(pred[0])
            unique_votes = set(class_predictions)
            yHat.append(max(unique_votes, key=class_predictions.count))
        return np.array(yHat)


def file_to_numpy(filename):
    """
    Read an input file and convert it to numpy
    """
    df = pd.read_csv(filename)
    return df.to_numpy()


def main():
    """
    Main file to run from the command line.
    """
    # set up the program to take in arguments from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("xTrain",
                        help="filename for features of the training data")
    parser.add_argument("yTrain",
                        help="filename for labels associated with training data")
    parser.add_argument("xTest",
                        help="filename for features of the test data")
    parser.add_argument("yTest",
                        help="filename for labels associated with the test data")
    parser.add_argument("epoch", type=int, help="max number of epochs")
    parser.add_argument("--seed", default=334, 
                        type=int, help="default seed number")
    
    args = parser.parse_args()
    # load the train and test data assumes you'll use numpy
    xTrain = file_to_numpy(args.xTrain)
    yTrain = file_to_numpy(args.yTrain)
    xTest = file_to_numpy(args.xTest)
    yTest = file_to_numpy(args.yTest)

    np.random.seed(args.seed)   
    #'''
    model = RandomForest(args.epoch, 6, "entropy", 5, 1)
    trainStats = model.train(xTrain, yTrain)
    print(trainStats)
    yHat_estimate = model.predict(xTrain)
    yHat = model.predict(xTest)
    oob_error = 1 - accuracy_score(yTest, yHat)
    oob_error_estimate = 1 - accuracy_score(yTrain, yHat_estimate)

    print(oob_error)
    print(oob_error_estimate)
    #'''

    ''' # BEST Params for inner DTC
    dt_classifier = DecisionTreeClassifier()
    param_grid = {
        'criterion': ['gini', 'entropy'],
        'max_depth': [None, 5, 10, 15],
        'min_samples_leaf': [1, 2, 4]
    }
    grid_search = GridSearchCV(estimator=dt_classifier, param_grid=param_grid, cv=5, scoring='accuracy')
    grid_search.fit(xTrain, yTrain)
    print("Best Parameters: ", grid_search.best_params_)
    print("Best Cross-validated Accuracy: {:.2f}".format(grid_search.best_score_))
    '''
    test_epochs= [x+1 for x in range(101)]
    oob_errors = []
    test_maxfeat= [x+1 for x in range(10)]
    oob_errors2 = []

    # for x in test_epochs:
    #     print(x)
    #     model = RandomForest(x, 3, "entropy", 5, 1)
    #     model.train(xTrain, yTrain)
    #     yHat = model.predict(xTest)
    #     oob_error = 1 - accuracy_score(yTest, yHat)
    #     oob_errors.append(oob_error)

    # for x in test_maxfeat:
    #     print(x)
    #     model = RandomForest(5, x, "entropy", 5, 1)
    #     model.train(xTrain, yTrain)
    #     yHat = model.predict(xTest)
    #     oob_error2 = 1 - accuracy_score(yTest, yHat)
    #     oob_errors2.append(oob_error2)

    # plt.plot(test_epochs, oob_errors, color='darkorange', label='Number of Trees Vs OOB Error')
    # plt.plot(test_maxfeat, oob_errors2, color='darkgreen', label='MaxFeat Vs OOB Error')
    # plt.show()

if __name__ == "__main__":
    main()

    # python rf.py q4xTrain.csv q4yTrain.csv q4xTest.csv q4yTest.csv 15