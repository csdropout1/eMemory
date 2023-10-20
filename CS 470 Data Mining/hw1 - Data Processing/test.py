import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r'final.csv')

df["Homework Mean"] = (df["Homework 1"] + df["Homework 2"] + df["Homework 3"] + df["Homework 4"] + df["Homework 5"])/5

#bx1 = df.boxplot(column=["Homework 1", "Homework 2", "Homework 3", "Homework 4", "Homework 5"])
#bx2 = df.boxplot(column=["Homework 1", "Homework 1 Rescaled", "Homework 1 Z score", "Homework 1 Semester Z Scores"])
#bx3 = df.boxplot(column=["Homework 1 Z score", "Homework 2 Z score", "Homework 3 Z score", "Homework 4 Z score", "Homework 5 Z score"])

#hx1 = df.hist(column=["Final Exam", "Total Score"])
#hx2 = df.hist(column=["Quiz 01", "Quiz 12"])
#hx3 = df.hist(column=["Homework 1", "Homework 5"])

#sx1 = df.plot.scatter("Homework 1", "Total Score")
#sx2 = df.plot.scatter("Quiz 01", "Total Score")
#sx3 = df.plot.scatter("Final Exam", "Total Score")

dx1 = df.plot.scatter("Homework Mean", "Total Score")


#plt.setp(bx3.get_xticklabels(), rotation=8, horizontalalignment='right')
plt.show()





