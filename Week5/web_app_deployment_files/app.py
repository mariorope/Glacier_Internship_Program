# Importing required packages
import numpy as np
from flask import Flask, request, render_template
import pickle

# Creating the Flask application
app=Flask(__name__)

# Importing the model previous created
model = pickle.load(open("model.pkl", "rb"))

# Creating the application routes including the home and predict paths
@app.route("/")
def home():
	return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
	
	# For rendering results on HTML GUI
	features = [[float(x) for x in request.form.values()]]
	prediction = model.predict(features)

	# Result of the prediction
	output = round(prediction[0], 1)

	# Creating a text for healthy and unhealthy levels of Diabets (Not true values adopted by the medicine field)
	if output == 0 :
		text = "This plant is from the Setosa species"
	elif output == 1:
		text = "This plant is from the Versicolor species"
	elif output == 1:
		text = "This plant is from the Virginica species"
	else:
		text = "This plant is unkown!"

	# Rendering the results of the prediction
	return render_template("index.html", prediction_text="{}.".format(text))

# Initializing the application
if __name__ == "__main__":
	app.run(port=5000, debug=True)