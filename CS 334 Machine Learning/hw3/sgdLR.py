import argparse
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt


from lr import LinearRegression, file_to_numpy
from standardLR import StandardLR

def grad_pt(beta, xi, yi):
    """
    Calculate the gradient for a mini-batch sample.

    Parameters
    ----------
    beta : 1d array with shape d
    xi : 2d numpy array with shape b x d
        Batch training data
    yi: 2d array with shape bx1
        Array of responses associated with training data.

    Returns
    -------
        grad : 1d array with shape d
    """
    # xi trans  * (yi - xiB)
    b = xi.shape[0]
    y_predict = np.matmul(xi, beta) 
    dif = yi - y_predict
    gradient = 1/b * np.matmul(np.transpose(xi), dif)

    return gradient


class SgdLR(LinearRegression):
    lr = 1  # learning rate
    bs = 1  # batch size
    mEpoch = 1000 # maximum epoch size

    def __init__(self, lr, bs, epoch):
        self.lr = lr
        self.bs = bs
        self.mEpoch = epoch

    def train_predict(self, xTrain, yTrain, xTest, yTest):
        """
        See definition in LinearRegression class
        """
        trainStats = {}
        # TODO: DO SGD
        xTrain = np.concatenate((np.ones((xTrain.shape[0], 1)), xTrain), axis=1)
        xTest = np.concatenate((np.ones((xTest.shape[0], 1)), xTest), axis=1)
        b_Train = (int)(len(xTrain)/self.bs)
        self.beta = np.zeros((xTrain.shape[1],1))

        for e in range(self.mEpoch):
            p = np.random.permutation(len(xTrain))
            data_x = xTrain[p]
            data_y = yTrain[p]

            for b in range(b_Train):
                start = time.time()
                index = b*self.bs
                end = index+self.bs
                subset_x = data_x[index:end]
                subset_y = data_y[index:end]
                self.beta = self.beta + self.lr * grad_pt(self.beta, subset_x, subset_y)
                mse_train = self.mse(xTrain, yTrain)
                mse_test = self.mse(xTest, yTest)
                t = time.time()-start
                trainStats[(e*b_Train)+b] = {'time': t, 'train-mse': mse_train, 'test-mse': mse_test}
            
        return trainStats


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
    parser.add_argument("lr", type=float, help="learning rate")
    parser.add_argument("bs", type=int, help="batch size")
    parser.add_argument("epoch", type=int, help="max number of epochs")
    parser.add_argument("--seed", default=334, 
                        type=int, help="default seed number")

    args = parser.parse_args()
    # load the train and test data
    xTrain = file_to_numpy(args.xTrain)
    yTrain = file_to_numpy(args.yTrain)
    xTest = file_to_numpy(args.xTest)
    yTest = file_to_numpy(args.yTest)

    # setting the seed for deterministic behavior
    '''
    np.random.seed(args.seed)   
    model = SgdLR(args.lr, args.bs, args.epoch)
    trainStats = model.train_predict(xTrain, yTrain, xTest, yTest)
    print(trainStats)
    '''

    # 3c
    '''
    p = np.random.permutation(len(xTrain))
    xTrain = xTrain[p]
    yTrain = yTrain[p]
    s1 = int(len(xTrain)*0.4)
    xTrain = xTrain[:s1]
    yTrain = yTrain[:s1]

    learning_rate = [0.1, 0.01, 0.001, 0.0001, 0.00001] # 0.00001 is best
    for lr in learning_rate:
        print(lr)
        model = SgdLR(lr, 1, args.epoch)
        trainStats = model.train_predict(xTrain, yTrain, xTest, yTest)
        test_mse = []
        r = np.arange(len(trainStats) / args.epoch, len(trainStats) + 1, len(trainStats) / args.epoch)
        for i in r:
            test_mse.append(trainStats[i - 1]['test-mse'])

        x_axis = [i for i in range(len(test_mse))]
        plt.plot(x_axis, test_mse, label='lr =' + str(lr))

    plt.legend()
    plt.xlabel('epochs')
    plt.ylabel('mse')
    plt.yscale('log')
    plt.show()
    '''

    # 3d
    '''
    model = SgdLR(args.lr, 1, args.epoch)
    trainStats = model.train_predict(xTrain, yTrain, xTest, yTest)
    test_mse = []
    train_mse = []
    r = np.arange(len(trainStats) / args.epoch, len(trainStats) + 1, len(trainStats) / args.epoch)
    for i in r:
        test_mse.append(trainStats[i - 1]['test-mse'])
        train_mse.append(trainStats[i - 1]['train-mse'])

    x_axis = [i for i in range(len(test_mse))]
    plt.plot(x_axis, test_mse, label='test-mse')

    x_axis = [i for i in range(len(train_mse))]
    plt.plot(x_axis, train_mse, label='train-mse')

    plt.legend()
    plt.xlabel('epochs')
    plt.ylabel('mse')
    #plt.yscale('log')
    plt.show()
    '''

    '''
    bs = [1, 10, 30, 559, 1667, 16670] 

    for b in bs:
        start = time.time()
        model = SgdLR(0.0001, b, args.epoch)
        trainStats = model.train_predict(xTrain, yTrain, xTest, yTest)
        test_mse_values = []  
        train_mse_values = []  
        times_values = []
        times = 0
        
        r = np.arange(len(trainStats) / args.epoch, len(trainStats) + 1, len(trainStats) / args.epoch)
        for i in r:
            test_mse_values.append(trainStats[i - 1]['test-mse'])
            train_mse_values.append(trainStats[i - 1]['train-mse'])
            times += (time.time()-start)
            times_values.append(times)
            print(times)
        
        plt.plot(times_values, test_mse_values, label=f'test-mse: batch size {b}')
        plt.plot(times_values, train_mse_values, label=f'train-mse: batch size {b}')


    model = StandardLR()
    trainStats = model.train_predict(xTrain, yTrain, xTest, yTest)

    plt.plot(trainStats[0]['time'], trainStats[0]['train-mse'], '^', label='train-mse close solution')
    plt.plot(trainStats[0]['time'], trainStats[0]['test-mse'], 'v', label='test-mse close solution')
    plt.legend()
    plt.xlabel('time')
    plt.ylabel('mse')
    plt.yscale('log')
    plt.xscale('log')
    plt.show()
    '''

if __name__ == "__main__":
    main()

