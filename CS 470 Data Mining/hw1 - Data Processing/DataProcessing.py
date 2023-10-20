import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r'grades.csv')
# Task 2 Re-encoding
for x in range(784):
    df["Semester"][x] = df["Semester"][x][1:3] + df["Semester"][x][0:1]

df = df.sort_values("Semester")

list = ["16F", "16S", "17F", "17S", "18F", "18S"]


for x in range(4,10):
    # Task 4 , A1
    col_name = df.columns[x]
    new_name = ""+col_name+ " Rescaled"
    df[new_name] = ((df[col_name]-df[col_name].min())/(df[col_name].max()-df[col_name].min()))*100

    # Task 4 , A2
    std = df[col_name].std()
    mean = df[col_name].mean()
    new_name2 = ""+col_name+ " Z score"
    df[new_name2] = (df[col_name]-mean)/std

    # Task 5
    min = df[col_name].min()
    max = df[col_name].max()
    sum = df[col_name].quantile([0.25,0.5,0.75])
    print(col_name+ " mean: ")
    print(mean)
    print(col_name + " std: ")
    print(std)
    print(col_name + " max and min: ")
    print(max)
    print(min)
    print(sum)

    # Task 4, A3
    new_name3 = "" + col_name + " Semester Z Scores"
    af = pd.DataFrame({
        'Student ID': []
    })

    for y in list:
        mf = df[df.Semester == y]
        means = mf[col_name].mean()
        stds = mf[col_name].std()
        mf[new_name3] = (mf[col_name] - means) / stds

        af = pd.merge(af, mf, how="outer")

    df = pd.merge(df, af, how="left")

for x in range(11,23):
    #Task 4 , A1
    col_name = df.columns[x]
    new_name = ""+col_name+ " Rescaled"
    df[new_name] = ((df[col_name]-df[col_name].min())/(df[col_name].max()-df[col_name].min()))*100

    # Task 4 , A2
    std = df[col_name].std()
    mean = df[col_name].mean()
    new_name2 = "" + col_name + " Z score"
    df[new_name2] = (df[col_name]-mean)/std

    # Task 5
    min = df[col_name].min()
    max = df[col_name].max()
    sum = df[col_name].quantile([0.25, 0.5, 0.75])
    print(col_name + " mean: ")
    print(mean)
    print(col_name + " std: ")
    print(std)
    print(col_name + " max and min: ")
    print(max)
    print(min)
    print(sum)

    # Task 4, A3
    new_name3 = "" + col_name + " Semester Z Scores"
    af = pd.DataFrame({
        'Student ID': []
    })

    for y in list:
        mf = df[df.Semester == y]
        means = mf[col_name].mean()
        stds = mf[col_name].std()
        mf[new_name3] = (mf[col_name] - means) / stds

        af = pd.merge(af, mf, how="outer")

    df = pd.merge(df, af, how="left")

for x in range(26,28):
    # Task 4 , A1
    col_name = df.columns[x]
    new_name = ""+col_name+ " Rescaled"
    df[new_name] = ((df[col_name]-df[col_name].min())/(df[col_name].max()-df[col_name].min()))*100

    # Task 4 , A2
    std = df[col_name].std()
    mean = df[col_name].mean()
    new_name2 = "" + col_name + " Z score"
    df[new_name2] = (df[col_name]-mean)/std

    #Task 5
    min = df[col_name].min()
    max = df[col_name].max()
    sum = df[col_name].quantile([0.25, 0.5, 0.75])
    print(col_name + " mean: ")
    print(mean)
    print(col_name + " std: ")
    print(std)
    print(col_name + " max and min: ")
    print(max)
    print(min)
    print(sum)

    # Task 4, A3
    new_name3 = "" + col_name + " Semester Z Scores"
    af = pd.DataFrame({
        'Student ID': []
    })

    for y in list:
        mf = df[df.Semester == y]
        means = mf[col_name].mean()
        stds = mf[col_name].std()
        mf[new_name3] = (mf[col_name] - means) / stds

        af = pd.merge(af, mf, how="outer")

    df = pd.merge(df, af, how="left")

#Task 5
for x in range(24,26):
    col_name = df.columns[x]
    std = df[col_name].std()
    mean = df[col_name].mean()
    min = df[col_name].min()
    max = df[col_name].max()
    sum = df[col_name].quantile([0.25, 0.5, 0.75])
    print(col_name + " mean: ")
    print(mean)
    print(col_name + " std: ")
    print(std)
    print(col_name + " max and min: ")
    print(max)
    print(min)
    print(sum)

#df.to_csv('final.csv')
#print(df.iloc[:, 4:9])
#print(df.iloc[:, 11:23])
#print(df.iloc[:, 24:26])

#bx = df.boxplot(column=["Homework 1", "Homework 2", "Homework 3", "Homework 4", "Homework 5"])
#bx2 = df.boxplot(column=["Homework 1", "Homework 1 Rescaled", "Homework 1 Z score", "Homework 1 Semester Z Scores"])
#bx3 = df.boxplot(column=["Homework 1 Z score", "Homework 2 Z score", "Homework 3 Z score", "Homework 4 Z score", "Homework 5 Z score"])
#bx.plot()
#print(bx)
#plt.show()
#fig.savefig("no2_concentrations.png")
