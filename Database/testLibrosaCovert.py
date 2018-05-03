import numpy as np
import scipy
import matplotlib.pyplot as plt
import sklearn.cluster
import librosa
import librosa.display
import tensorflow as tf
import os
import wave
import contextlib
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from  keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras.models import load_model
import keras
# Reverse arrays for 2dConv Layer
from keras import backend as K
K.set_image_dim_ordering('th')

# Time at which frequency matrix is obtained
timeOffset = .5
timeDuration = 1.5

def get_files():
  files = []
  for (path, dirnames, filenames) in os.walk('Training'):
    files.extend(os.path.join(path, name) for name in filenames)
  return files


def WeedOutBadWav(files):
	good_files = []
	i = 0
	for file in files:
		with contextlib.closing(wave.open(file,'r')) as f:
			frames = f.getnframes()
			rate = f.getframerate()
			dur = frames / float(rate)
			# y, sr = librosa.load(file)
			# dur = librosa.get_duration(y=y, sr=sr)
			if (dur > 3):
				good_files.append(file)
			if i % 250 is 0:
				print("Completed duration test for files: %d" % i)
		i+=1
	np.savez("GoodFilesArray", good_files)
	return good_files

def GetFrequencyMatrix(fileLocation, tOffset, tDuration):
	y, sr = librosa.load(fileLocation, offset = tOffset, duration = tDuration)
	frequency, D = librosa.ifgram(y, sr=sr)
	print("Frequency obtained for %s" % fileLocation)
	# print(frequency.shape)
	return frequency

def GetAllFreqency():
	with np.load("GoodFilesArray.npz") as data:
		files = data['arr_0']
	# if size > 10000:
	# 	it = 0
	# 	while size > 10000:
	# 		filename = "FeaturesAndLabels" + it

	# 		it += 1
	# size = len(files)
	size = 30000
	features = np.zeros((size, 1025, 65),dtype=np.float32)
	labels = np.zeros(size)
	i = 0
	while i < size:
		freq = GetFrequencyMatrix(files[i], timeOffset, timeDuration)
		# if freq.shape == np.zeros((1025,65)).shape:
		features[i] = freq
		if 'female' in files[i]:
			labels[i] = 0
		else:
			labels[i] = 1
		i += 1
		# else:
		# 	print("Not proper size")
	np.savez("FeaturesAndLabels", features, labels)

def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]

def TrainModel(epoch, batch_size):
	# Load numpy array
	with np.load("FeaturesAndLabels.npz") as data:
		X_train = data['arr_0']
		y_train = data['arr_1']

	X_train, y_train= unison_shuffled_copies(X_train,y_train)
	print(X_train[:10])
	print(y_train[:10])
	# Split input data
	X_test = X_train[:(int)(len(X_train)/3)]
	X_train = X_train[(int)(len(X_train)/3):len(X_train)]
	# Split input data
	y_test = y_train[:(int)(len(y_train)/3)]
	y_train = y_train[(int)(len(y_train)/3):len(y_train)]

	## PLOT OF FREQUENCY AT ONE SEC ##
	# print(X_train[0][0].shape)
	# plt.plot(X_train[0][0])
	# plt.show()

	# Reshape input data
	X_train = X_train.reshape(X_train.shape[0], 1, 1025, 65)
	X_test = X_test.reshape(X_test.shape[0], 1, 1025, 65)
	print(X_train.shape)

	# Convert data type and normalize values
	X_train = X_train.astype('float32')
	X_test = X_test.astype('float32')
	# X_train /= 255
	# X_test /= 255

	# Preprocess class labels
	Y_train = np_utils.to_categorical(y_train, 2)
	Y_test = np_utils.to_categorical(y_test, 2)
	print(Y_train.shape)

	# Building model/adding layers
	model = Sequential()
	# model.add(Convolution2D(32, 3, 3, activation='relu', input_shape=(1,1025,65)))
	# # print(model.output_shape)
	# model.add(Convolution2D(32, 3, 3, activation='relu'))
	# model.add(MaxPooling2D(pool_size=(2,2)))
	# model.add(Dropout(0.25))
	# model.add(Flatten())
	# model.add(Dense(128, activation='relu'))
	# model.add(Dropout(0.5))
	# model.add(Dense(2, activation='softmax'))
	# model.compile(loss='categorical_crossentropy',
	#               optimizer='adam',
	#               metrics=['accuracy'])
	# model.fit(X_train, Y_train, batch_size=32, nb_epoch=3, verbose=1)
	model = Sequential()
	model.add(Convolution2D(32, kernel_size=(5, 5), strides=(1, 1),
	                 activation='relu',
	                 input_shape=(1,1025,65)))
	model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
	model.add(Convolution2D(64, (5, 5), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Flatten())
	model.add(Dense(1000, activation='relu'))
	model.add(Dense(2, activation='softmax'))
	model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.SGD(lr=0.01),
              metrics=['accuracy'])
	model.fit(X_train, Y_train,
          batch_size=batch_size,
          epochs=epoch,
          verbose=1,
          validation_data=(X_test, Y_test))
	model.save('my_model.h5')
	score = model.evaluate(X_test, Y_test, verbose=0)
	print('Test loss:', score[0])
	print('Test accuracy:', score[1])
	## TEST MODEL WITH ONE DATA POINT ##
	# testItem = GetFrequencyMatrix("AlexVoice.wav", timeOffset, timeDuration)
	# prediciton = model.predict(testItem, batch_size=None, verbose=0, steps=None)
	# print(prediciton)

## GET AND SAVE NPZ FILE OF FILES OVER FIXED SECONDS ##
good_files = WeedOutBadWav(get_files())

## GET FREQUENCY AND SAVE TO NPZ FILE ##
GetAllFreqency()

## TRAIN MODEL ##
TrainModel(10, 32)

## LOAD AND TEST MODEL ##
model = load_model('my_model.h5')
testItem = GetFrequencyMatrix("AlexVoice.wav", timeOffset, timeDuration)
testItem = testItem.reshape(1, 1025, 65)
testItem = testItem.reshape(testItem.shape[0],1, 1025, 65)
testItem = testItem.astype('float32')
# testItem /= 255
print(testItem.shape)
print(testItem)
prediciton = model.predict_proba(testItem, batch_size=None, verbose=0, steps=None)
print(prediciton[0])
testItem = GetFrequencyMatrix("test/female/sample-000026.wav", timeOffset, timeDuration)
testItem = testItem.reshape(1, 1025, 65)
testItem = testItem.reshape(testItem.shape[0],1, 1025, 65)
testItem = testItem.astype('float32')
# testItem /= 255
print(testItem)
print(testItem.shape)
prediciton = model.predict_proba(testItem, batch_size=None, verbose=0, steps=None)
print(prediciton[0])
