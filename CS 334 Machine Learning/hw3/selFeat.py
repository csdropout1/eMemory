import argparse
import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

'''
maybe day
hour --> time of day, dif engery
'''
def extract_features(df):
    """
    Given a pandas dataframe, extract the relevant features
    from the date column

    Parameters
    ----------
    df : pandas dataframe
        Training or test data 
    Returns
    -------
    df : pandas dataframe
        The updated dataframe with the new features
    """
    # TODO do more than this
    # df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y %H:%M')
    # df['dat', 'time'] = df['date'].str.split(' ')
    # df['day'] = df['dat', 'time'].str[0].str.split('/').str[1].astype(int)
    # df['hour'] = df['dat', 'time'].str[1].str.split(':').str[0].astype(int)

    # df = df.drop(columns=['date', ('dat', 'time')])

    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y %H:%M')
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour

    df = df.drop(columns=['date'])
    return df


def cal_corr(df):
    """
    Given a pandas dataframe (include the target variable at the last column), 
    calculate the correlation matrix (compute pairwise correlation of columns)

    Parameters
    ----------
    df : pandas dataframe
        Training or test data (with target variable)
    Returns
    -------
    corrMat : pandas dataframe
        Correlation matrix
    """
    # TODO
    # m, n = df.shape
    # def covariance(x, y):
    #     x_, y_ = x.mean(), y.mean()
    #     x = x -x_
    #     y = y -y_
    #     return float(np.sum(x*y))
    
    # def stan_(a):
    #     a_ = a.mean()
    #     a = a-a_
    #     return float(np.sqrt(np.sum(a*a)))
    # list_of_lists = [[0]*(n) for _ in range(n)]

    # for c in range(n):
    #     for c2 in range(n):
    #         temp = covariance(df.iloc[:, c], df.iloc[:, c2])
    #         a = stan_(df.iloc[:, c]) * stan_(df.iloc[:, c2])
    #         temp = (temp/a)
    #         list_of_lists[c][c2] = temp
    
    # corrMat = pd.DataFrame(list_of_lists)
    # corrMat.columns = df.columns 

    ### Same result but faster...
    corrMat = df.corr(method='pearson')
    return corrMat

def select_features(df):
    """
    Select the features to keep

    Parameters
    ----------
    df : pandas dataframe
        Training or test data 
    Returns
    -------
    df : pandas dataframe
        The updated dataframe with a subset of the columns
    """
    # TODO
    df = df[["lights", "T2", "hour"]]
    return df


def preprocess_data(trainDF, testDF):
    """
    Preprocess the training data and testing data

    Parameters
    ----------
    trainDF : pandas dataframe
        Training data 
    testDF : pandas dataframe
        Test data 
    Returns
    -------
    trainDF : pandas dataframe
        The preprocessed training data
    testDF : pandas dataframe
        The preprocessed testing data
    """
    # TODO do something
    m1, n1 = trainDF.shape
    m2, n2 = testDF.shape

    for col in trainDF:
        m = np.mean(trainDF[col])
        std = np.std(trainDF[col])
        for v in range(m1):
            trainDF[col][v] = (trainDF[col][v]-m)/std

    for col in testDF:
        m = np.mean(testDF[col])
        std = np.std(testDF[col])
        for v in range(m2):
            testDF[col][v] = (testDF[col][v]-m)/std
    
    return trainDF, testDF


def main():
    """
    Main file to run from the command line.
    """
    # set up the program to take in arguments from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("outTrain",
                         help="filename of the updated training data")
    parser.add_argument("outTest",
                         help="filename of the updated test data")
    parser.add_argument("--trainFile",
                        default="eng_xTrain.csv",
                        help="filename of the training data")
    parser.add_argument("--testFile",
                        default="eng_xTest.csv",
                        help="filename of the test data")
    parser.add_argument("--yTrainFile",
                        default="eng_yTrain.csv",
                        help="filename of the training data")
    args = parser.parse_args()
    # load the train and test data
    xTrain = pd.read_csv(args.trainFile)
    xTest = pd.read_csv(args.testFile)
    # extract the new features
    xNewTrain = extract_features(xTrain)
    xNewTest = extract_features(xTest)

    # select the features

    ''' # for the heatmap stuff. . . 
    yTrain = pd.read_csv(args.yTrainFile)
    xNewTrain['target'] = yTrain['label'] 
    print(xNewTrain)
    sns.heatmap(cal_corr(xNewTrain), annot=True, cmap='coolwarm',fmt=".2f")
    plt.xticks(range(len(xNewTrain.columns)), labels=xNewTrain.columns)
    plt.yticks(range(len(xNewTrain.columns)), labels=xNewTrain.columns)
    plt.show()
    '''

    
    xNewTrain = select_features(xNewTrain)
    xNewTest = select_features(xNewTest)
    # preprocess the data
    xTrainTr, xTestTr = preprocess_data(xNewTrain, xNewTest)
    
    # save it to csv
    xTrainTr.to_csv(args.outTrain, index=False)
    xTestTr.to_csv(args.outTest, index=False)
    

if __name__ == "__main__":
    main()
