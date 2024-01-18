import argparse
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

from sklearn.tree import DecisionTreeClassifier

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
    '''
    dtc = DecisionTreeClassifier(criterion='gini', max_depth=args.md, min_samples_leaf=args.mls)
    dtc.fit(xTrain, yTrain)
    trainAcc1, testAcc1 = accuracy_score(yTrain, dtc.predict(xTrain)), accuracy_score(yTest, dtc.predict(xTest))
    print("GINI Criterion ---------------")
    print("Training Acc:", trainAcc1)
    print("Test Acc:", testAcc1)
    dt = DecisionTreeClassifier(criterion='entropy', max_depth=args.md, min_samples_leaf=args.mls)
    dt.fit(xTrain, yTrain)
    trainAcc, testAcc = accuracy_score(yTrain, dt.predict(xTrain)), accuracy_score(yTest, dt.predict(xTest))
    print("Entropy Criterion ---------------")
    print("Training Acc:", trainAcc)
    print("Test Acc:", testAcc)
    '''
    
    md = args.md
    mls = args.mls

    gini_trainings = []
    gini_testings = []
    entropy_trainings = []
    entropy_testings = []

    for i in range(md):
        i += 2
        dt = DecisionTreeClassifier(criterion='entropy', max_depth=i, min_samples_leaf=2)
        dtc = DecisionTreeClassifier(criterion='gini', max_depth=i, min_samples_leaf=2)
        dt.fit(xTrain, yTrain)
        dtc.fit(xTrain, yTrain)
        trainAcc, testAcc = accuracy_score(yTrain, dt.predict(xTrain)), accuracy_score(yTest, dt.predict(xTest))
        trainAcc1, testAcc1 = accuracy_score(yTrain, dtc.predict(xTrain)), accuracy_score(yTest, dtc.predict(xTest))

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
        dt = DecisionTreeClassifier(criterion='entropy', max_depth=4, min_samples_leaf=mls)
        dtc = DecisionTreeClassifier(criterion='gini', max_depth=4, min_samples_leaf=mls)
        dt.fit(xTrain, yTrain)
        dtc.fit(xTrain, yTrain)
        trainAcc, testAcc = accuracy_score(yTrain, dt.predict(xTrain)), accuracy_score(yTest, dt.predict(xTest))
        trainAcc1, testAcc1 = accuracy_score(yTrain, dtc.predict(xTrain)), accuracy_score(yTest, dtc.predict(xTest))

        entropy_trainings.append(trainAcc)
        entropy_testings.append(testAcc)
        gini_trainings.append(trainAcc1)
        gini_testings.append(testAcc1)

    d = pd.DataFrame({'GINI Test': gini_testings, 'GINI Train': gini_trainings, 'Entropy Test': entropy_testings, 'Entropy Train': entropy_trainings})
    d.plot.line()
    plt.show()
    

if __name__ == "__main__":
    main()
