import pandas as pd
import sklearn.datasets 
import matplotlib.pyplot as plt

def load_iris(): #loading
    iris = sklearn.datasets.load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    return df

def main():
    df = load_iris()

    #boxplots
    for col in df:
        if col != 'target':
            bp = pd.DataFrame.boxplot(df,col,'target')
            pd.DataFrame.plot(bp)
    #scatterplots
    colors = {0:"green", 1:"red", 2:"blue"}
    #petal
    df1 = df.iloc[:,[0,1,4]].copy()
    df1.plot.scatter(x=0, y=1, color=df1['target'].map(colors))
    #sepal
    df2 = df.iloc[:, 2:5].copy()
    df2.plot.scatter(x=0, y=1, color=df2['target'].map(colors))
    #plt.show()

if __name__ == "__main__":
    main()