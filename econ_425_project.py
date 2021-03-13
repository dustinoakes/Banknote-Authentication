# -*- coding: utf-8 -*-
"""Econ 425 Project

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XnIC_K_SeEWuhRAjWhI64TEqaeHSlEvO

# **Banknote Authentication Project**
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

"""## **Importing Data**"""

df = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/00267/data_banknote_authentication.txt", header = None)

# Target Variable: class 0 is “genuine/authentic” and class 1 is “forgery/fake”
df = df.rename(columns={0: "Variance", 1: "Skewness", 2: "Kurtosis", 3: "Entropy", 4: "Target"})

X = df[["Variance", "Skewness", "Kurtosis", "Entropy"]]
y = df[["Target"]]
X = X.to_numpy()
y = y.to_numpy()

df

"""

---



## **Logistic Regression**
"""

#add data exploration

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

clf = LogisticRegression(random_state=0).fit(X_train, y_train.ravel())
clf.predict(X_test[:2, :])
clf.predict_proba(X_test[:2, :])
print("Score:", clf.score(X_test, y_test))

confusion_matrix(y_test, clf.predict(X_test))
#add validation

"""- True Negatives: 227 (correctly identified as real - successful)
- False Negatives: 0 (falsely identified as real - counterfeit money accepted)
- False Positives: 5 (falsely identified as fake - genuine money turned down)
- True Postivies: 180 (correctly identified as fake - successful)
"""

cm = confusion_matrix(y_test, clf.predict(X_test))

fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(cm)
ax.grid(False)
ax.xaxis.set(ticks=(0, 1), ticklabels=('Predicted 0s', 'Predicted 1s'))
ax.yaxis.set(ticks=(0, 1), ticklabels=('Actual 0s', 'Actual 1s'))
ax.set_ylim(1.5, -0.5)
for i in range(2):
    for j in range(2):
        ax.text(j, i, cm[i, j], ha='center', va='center', color='red')
plt.show()

"""# Attempt at Random Forest"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

rfclf=RandomForestClassifier(n_estimators=100)
rfclf.fit(X_train,y_train.ravel())

rf_y_pred=rfclf.predict(X_test)

print("Accuracy:",metrics.accuracy_score(y_test.ravel(), rf_y_pred.ravel()))

c = ["Variance", "Skewness", "Kurtosis", "Entropy"]
feature_imp = pd.Series(rfclf.feature_importances_,index=c).sort_values(ascending=False)

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
# Creating a bar plot
sns.barplot(x=feature_imp, y=feature_imp.index)
# Add labels to your graph
plt.xlabel('Feature Importance Score')
plt.ylabel('Features')
plt.title("Visualizing Important Features")
plt.legend()
plt.show()