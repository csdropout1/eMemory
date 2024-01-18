import argparse
import numpy as np
import pandas as pd
import time

from lr import LinearRegression, file_to_numpy


class StandardLR(LinearRegression):

    # self . beta for coeff

    def train_predict(self, xTrain, yTrain, xTest, yTest):
        """
        See definition in LinearRegression class
        """
        trainStats = {}
        # TODO: DO SOMETHING
        xTrain = np.concatenate((np.ones((xTrain.shape[0], 1)), xTrain), axis=1)
        xTest =  np.concatenate((np.ones((xTest.shape[0], 1)), xTest), axis=1)

        start = time.time()
        self.make_beta(xTrain, yTrain)
        mse_train = self.mse(xTrain, yTrain)
        mse_test = self.mse(xTest, yTest)
        t = time.time()-start
        trainStats[0] = {'time': t, 'train-mse': mse_train, 'test-mse': mse_test}

        return trainStats

    def make_beta(self, x, y): 
        x_trans = np.transpose(x)
        # formula in powerpoint
        self.beta = np.matmul(np.linalg.inv(np.matmul(x_trans,x)), np.matmul(x_trans, y))
        
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

    args = parser.parse_args()
    # load the train and test data
    xTrain = file_to_numpy(args.xTrain)
    yTrain = file_to_numpy(args.yTrain)
    xTest = file_to_numpy(args.xTest)
    yTest = file_to_numpy(args.yTest)

    model = StandardLR()
    trainStats = model.train_predict(xTrain, yTrain, xTest, yTest)
    print(trainStats)


if __name__ == "__main__":
    main()
