import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn.metrics as metrics

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import train_test_split
from keras.utils import to_categorical

import keras
from keras.layers import Dense
from keras.models import Sequential
from keras.callbacks import History
from keras.utils import plot_model
from keras.optimizers import SGD
from keras.models import load_model

def TrainModel():
	#Import and split data
	data = pd.read_csv('Features.csv')


	"""Model Building"""
	#Split features and labels
	x = data.iloc[:, :-1].values
	y = data.iloc[:,-1].values


	gender_encoder = LabelEncoder()
	y = gender_encoder.fit_transform(y) #Male = 1 ----- Female = 0

	#Preprocessess data
	scaler = StandardScaler()
	x = scaler.fit_transform(x)
	print(x[0])
	#Test-train split
	x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = .1)

	#Build Neural Network

	n_cols = x_train.shape[1]
	y_train = to_categorical(y_train, 2)

	hist = History()
	print(x_test.shape)

	model = Sequential()

	model.add(Dense(1000, activation='relu', input_dim = n_cols))
	model.add(Dense(1000, activation='relu'))
	model.add(Dense(1000, activation='relu'))
	model.add(Dense(1000, activation='relu'))


	model.add(Dense(2, activation='softmax'))

	model.compile(optimizer='adam',
	              loss='binary_crossentropy',
	              metrics=['accuracy'])

	model.fit(x_train, y_train, epochs = 40, validation_split = .1, callbacks = [hist])

	y_pred =  model.predict(x_test)
	y_pred = np.round(y_pred[:,1])
	print(metrics.accuracy_score(y_pred,y_test))

	plt.plot(hist.history['acc'], color = 'red')
	plt.plot(hist.history['val_acc'], color = 'blue')
	plt.xlabel('Epochs')
	plt.ylabel('Loss')
	model.save("Model.h5")

def TestModel(filepath):
	model = load_model("Model.h5")
	x = pd.read_csv(filepath)
	data_test = x.iloc[:, :].values
	pred = model.predict(data_test)
	return pred[0]

# TrainModel()
print(TestModel('Training/female/Output.csv'))
