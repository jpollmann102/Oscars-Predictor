import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression

# load in data
movies = pd.read_csv("data/cleaned.csv")
winners = pd.read_csv("data/winners.csv")

# drop the title name, but keep track of it
titles = movies['Title']
movies.drop(columns=['Title'], inplace=True)

xTrain, xTest, yTrain, yTest = train_test_split(movies, winners, random_state=1)

xTrain.drop(xTrain.columns[0], axis=1, inplace=True)
xTest.drop(xTest.columns[0], axis=1, inplace=True)
yTrain.drop(yTrain.columns[0], axis=1, inplace=True)
yTest.drop(yTest.columns[0], axis=1, inplace=True)

logreg = LogisticRegression(solver='lbfgs', max_iter=4000)
logreg.fit(xTrain, yTrain)
score = logreg.score(xTest, yTest)
print("\nAccuracy for predicting an Oscar winner was: {:.2f}%".format(score * 100))
