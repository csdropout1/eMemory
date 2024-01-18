import argparse
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, roc_auc_score

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def normalize_feat(xTrain, xTest):
    scaler = StandardScaler()
    xTrain = scaler.fit_transform(xTrain)
    xTest = scaler.fit_transform(xTest)

    return xTrain, xTest

def unreg_log(xTrain, yTrain, xTest, yTest):
    logreg = LogisticRegression(penalty='none', random_state=42)
    logreg.fit(xTrain, yTrain)
    y_probs = logreg.predict_proba(xTest)[:, 1]
    fpr, tpr, thresholds = roc_curve(yTest, y_probs)
    auc_value = roc_auc_score(yTest, y_probs)

    return fpr, tpr, auc_value

def run_pca(xTrain, xTest): # assume already normallized from top
    pca = PCA()
    xTrain_pca = pca.fit_transform(xTrain)
    cumulative_variance = np.cumsum(pca.explained_variance_ratio_)
    num_components_95 = np.argmax(cumulative_variance >= 0.95) + 1

    pca = PCA(n_components=num_components_95)
    xTrain_pca = pca.fit_transform(xTrain)
    xTest_pca = pca.transform(xTest)

    principal_components = pca.components_

    print(f"Number of components to capture at least 95% of the variance: {num_components_95}")
    print("Characteristics of the first three principal components:")
    for i in range(3):
        if i == num_components_95:
            break
        print(f"Principal Component {i + 1}: {principal_components[i]}")

    return xTrain_pca, xTest_pca, principal_components

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
    yTrain = pd.read_csv(args.yTrain).to_numpy()
    xTest = pd.read_csv(args.xTest).to_numpy()
    yTest = pd.read_csv(args.yTest).to_numpy()

    print(yTrain.shape, yTest.shape)

    xTrain, xTest = normalize_feat(xTrain, xTest)
    xTrain_pca, xTest_pca, principal_components = run_pca(xTrain, xTest)

    # Logistic Regression without regularization
    fpr, tpr, auc = unreg_log(xTrain_pca, yTrain, xTest_pca, yTest)
    fpr2, tpr2, auc = unreg_log(xTrain, yTrain, xTest, yTest)

    # Plot ROC Curve
    plt.figure(figsize=(8, 8))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve - PCA')
    plt.plot(fpr2, tpr2, color='darkgreen', lw=2, label='ROC curve - Not PCA')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curves')
    plt.legend(loc='lower right')
    plt.show()

if __name__ == "__main__":
    main()
