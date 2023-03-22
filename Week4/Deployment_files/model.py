#### Development of Predictive Classification Model using SVM for the Iris dataset ####

# This model was created based on the iris dataset, which is provided with the package sklearn.
# There are four variables, including the sepal length, sepal width, petal length and petal width (all in cm) and 150 records.
# In total there are three different species, which includes setosa, versicolor and virginica.

# Load packages
import random
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Load the diabetes dataset
iris_X, iris_y = datasets.load_iris(return_X_y=True)

# Creating random indexes for the traning set
train_indexes = random.sample(range(0, 150), 120)

# Split the data into training/testing sets
iris_X_train = iris_X[train_indexes,:]
iris_X_test = np.delete(iris_X, train_indexes, 0)

# Split the targets into training/testing sets
iris_y_train = iris_y[train_indexes]
iris_y_test = np.delete(iris_y, train_indexes)

# Create support vector machine (SVC) classifier
svn = SVC()

# Train the model using the training sets
svn.fit(iris_X_train, iris_y_train)

# Make predictions using the testing set
iris_y_pred = svn.predict(iris_X_test)


accuracy = accuracy_score(iris_y_test, iris_y_pred)

# The accuracy of the model
print("Accuracy of Model: \n", accuracy)

# Saving the model using pickle
with open("model.pkl", "wb") as f:
    pickle.dump(svn, f)