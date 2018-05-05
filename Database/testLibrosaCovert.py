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
from sklearn.model_selection import train_test_split
# Reverse arrays for 2dConv Layer
# from keras import backend as K
# K.set_image_dim_ordering('th')

# Time at which frequency matrix is obtained
timeOffset = .5
timeDuration = 2
DATA_PATH = "Training/"

def get_files(foldername):
  files = []
  for (path, dirnames, filenames) in os.walk(foldername):
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

def GetQuadratic(fileLocation, tOffset, tDuration):
  y, sr = librosa.load(fileLocation, offset = tOffset, duration = tDuration)
  S = np.abs(librosa.stft(y))
  quadratic = librosa.feature.poly_features(S=S, order=2)
  print("Quadratic obtained for %s" % fileLocation)
  return quadratic

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
  #   it = 0
  #   while size > 10000:
  #     filename = "FeaturesAndLabels" + it

  #     it += 1
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
    #   print("Not proper size")
  np.savez("FeaturesAndLabels", features, labels)

def GetAllQuadratic():
  with np.load("GoodFilesArray.npz") as data:
    files = data['arr_0']
  size = len(files)
  features = np.zeros((size, 3, 87),dtype=np.float32)
  labels = np.zeros(size)
  i = 0
  while i < size:
    quad = GetQuadratic(files[i], timeOffset, timeDuration)
    features[i] = quad
    if 'female' in files[i]:
      labels[i] = 0
    else:
      labels[i] = 1
    i += 1
  np.savez("QuadraticFeatureAndLabels", features, labels)

def WavToMFCC(file_path, tOffset=timeOffset, tDuration=timeDuration, max_pad_len=11):
  wave, sr = librosa.load(file_path, mono=True, sr=None, offset = tOffset, duration = tDuration)
  wave = wave[::3]
  mfcc = librosa.feature.mfcc(wave, sr=16000)
  # pad_width = max_pad_len - mfcc.shape[1]
  # mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')
  return mfcc

def get_labels(path=DATA_PATH):
  labels = os.listdir(path)
  label_indices = np.arange(0, len(labels))
  return labels, label_indices, keras.utils.to_categorical(label_indices)

def save_data_to_array(path=DATA_PATH, max_pad_len=11):
  labels, _, _ = get_labels(path)
  for label in labels:
        # Init mfcc vectors
    mfcc_vectors = []

    wavfiles = [path + label + '/' + wavfile for wavfile in os.listdir(path + '/' + label)]
    for wavfile in wavfiles:
        with contextlib.closing(wave.open(wavfile,'r')) as f:
          frames = f.getnframes()
          rate = f.getframerate()
          dur = frames / float(rate)
          # y, sr = librosa.load(file)
          # dur = librosa.get_duration(y=y, sr=sr)
          if (dur > 3):
            mfcc = WavToMFCC(wavfile)
            mfcc_vectors.append(mfcc)
            print(wavfile + ", appended to array")
    np.save(label + '.npy', mfcc_vectors)
    print(label + ", saved to npy")

# test=np.load("female.npy")
# print(test.shape)

def get_train_test(split_ratio=0.6, random_state=42):
    # Get available labels
    labels, indices, _ = get_labels(DATA_PATH)

    # Getting first arrays
    X = np.load(labels[0] + '.npy')
    y = np.zeros(X.shape[0])

    # Append all of the dataset into one single array, same goes for y
    for i, label in enumerate(labels[1:]):
        x = np.load(label + '.npy')
        X = np.vstack((X, x))
        y = np.append(y, np.full(x.shape[0], fill_value= (i + 1)))

    assert X.shape[0] == len(y)
    return train_test_split(X, y, test_size= (1 - split_ratio), random_state=random_state, shuffle=True)

def NewTrainmodel():
  X_train, X_test, y_train, y_test = get_train_test()
  X_train = X_train.reshape(X_train.shape[0], 20, 63, 1)
  X_test = X_test.reshape(X_test.shape[0], 20, 63, 1)
  y_train_hot = keras.utils.to_categorical(y_train)
  y_test_hot = keras.utils.to_categorical(y_test)
  model = Sequential()
  model.add(Convolution2D(32, kernel_size=(2, 2), activation='relu', input_shape=(20, 63, 1)))
  model.add(MaxPooling2D(pool_size=(2, 2)))
  model.add(Dropout(0.25))
  model.add(Flatten())
  model.add(Dense(128, activation='relu'))
  model.add(Dropout(0.25))
  model.add(Dense(2, activation='softmax'))
  model.compile(loss=keras.losses.categorical_crossentropy,
                optimizer=keras.optimizers.Adadelta(),
                metrics=['accuracy'])
  model.fit(X_train, y_train_hot, batch_size=100, epochs=100, verbose=1, validation_data=(X_test, y_test_hot))
  model.save("NewTrainmodel.h5")

# NewTrainmodel()
def TestWavAgainstModel(filepath,modelpath):
  model = load_model(modelpath)
  sample = WavToMFCC(filepath)
  sample_reshaped = sample.reshape(1, 20, 63, 1)
  print((model.predict_proba(sample_reshaped)))
  del model

# TestWavAgainstModel("test/sample-000010.wav","NewTrainmodel.h5")

def unison_shuffled_copies(a, b):
  assert len(a) == len(b)
  p = np.random.permutation(len(a))
  return a[p], b[p]

def TrainModel(data_file,epoch, batch_size):
  # Load numpy array
  with np.load(data_file) as data:
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

  # Reshape input data
  X_train = X_train.reshape(X_train.shape[0], 1, 3, 87)
  X_test = X_test.reshape(X_test.shape[0], 1, 3, 87)
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
  # model.add(Convolution2D(32, (3, 3), activation='relu', input_shape=(1,3,87), data_format='channels_first'))
  model = Sequential()
  model.add(Convolution2D(32, kernel_size=(2, 2), activation='relu', input_shape=(1,3,87)))
  model.add(MaxPooling2D(pool_size=(2, 2)))
  model.add(Dropout(0.25))
  model.add(Flatten())
  model.add(Dense(128, activation='relu'))
  model.add(Dropout(0.25))
  model.add(Dense(2, activation='softmax'))
  model.compile(loss=keras.losses.categorical_crossentropy,
          optimizer=keras.optimizers.Adadelta(),
          metrics=['accuracy'])
  # model.add(Convolution2D(32, 1, 1, activation='relu', input_shape=(1,3,87)))
  # model.add(Convolution2D(32, 1, 1, activation='relu'))
  # model.add(MaxPooling2D(pool_size=(1,1)))
  # model.add(Dropout(0.25))

  # model.add(Flatten())
  # model.add(Dense(128, activation='relu'))
  # model.add(Dropout(0.5))
  # model.add(Dense(2, activation='softmax'))
  # model.compile(loss='categorical_crossentropy',
  #               optimizer='adam',
  #               metrics=['accuracy'])
  model.fit(X_train, Y_train, batch_size=32, nb_epoch=3, verbose=1)

  model.save('my_model2.h5')
  score = model.evaluate(X_test, Y_test, verbose=0)
  print('Test loss:', score[0])
  print('Test accuracy:', score[1])

# def TestWavAgainstModel(filepath,modelpath):
#   model = load_model(modelpath)
#   testItem = GetQuadratic(filepath, timeOffset, timeDuration)
#   testItem = testItem.reshape(1, 3, 87)
#   testItem = testItem.reshape(testItem.shape[0],1, 3, 87)
#   testItem = testItem.astype('float32')
#   prediciton = model.predict(testItem, batch_size=None, verbose=0, steps=None)
#   print(filepath + " prediction: ")
#   print(prediciton[0])
#   del model
## GET AND SAVE NPZ FILE OF FILES OVER FIXED SECONDS ##
# good_files = WeedOutBadWav(get_files("Training"))

## GET FREQUENCY AND SAVE TO NPZ FILE ##
# GetAllQuadratic()
# GetAllFreqency()

## TRAIN MODEL ##
# TrainModel("QuadraticFeatureAndLabels.npz", 2, 32)

## LOAD AND TEST MODEL ##
# TestWavAgainstModel("test/sample-000017.wav","my_model2.h5")
# TestWavAgainstModel("test/sample-000010.wav","my_model2.h5")



# model = load_model('my_model.h5')
# testFiles = get_files('test')
# test_array = np.zeros((len(testFiles), 3, 87),dtype=np.float32)
# i = 0
# for file in testFiles:
#   test = GetQuadratic(file,timeOffset,timeDuration)
#   if test.shape == np.zeros((3,87)):
#     test_array[i] = test
#   i += 1
# print(test_array.shape)
# test_array = test_array.reshape(test_array.shape[0], 1, 3, 87)
# test_array = test_array.astype('float32')
# prediciton = model.predict(test_array, batch_size=32, verbose=2, steps=None)
# print(prediciton)


# testItem = GetQuadratic("test/sample-000017.wav", timeOffset, timeDuration)
# testItem = testItem.reshape(1, 3, 87)
# testItem = testItem.reshape(testItem.shape[0],1, 3, 87)
# testItem = testItem.astype('float32')
# prediciton = model.predict(testItem, batch_size=None, verbose=0, steps=None)
# print(prediciton[0])

# testItem = GetQuadratic("test/female/sample-004092.wav", timeOffset, timeDuration)
# testItem = testItem.reshape(1, 3, 87)
# testItem = testItem.reshape(testItem.shape[0],1, 3, 87)
# testItem = testItem.astype('float32')
# prediciton = model.predict(testItem, batch_size=None, verbose=0, steps=None)
# print(prediciton[0])





## TRYING TO AVERAGE A MATRIX ##
# y, sr = librosa.load("Training/male/sample-000019.wav",offset=.5,duration=2)
# S = np.abs(librosa.stft(y))
# p2 = librosa.feature.poly_features(S=S, order=2)
# ax = plt.subplot(4,1,1)
# plt.subplot(4,1,3, sharex=ax)
# plt.plot(p2[0], label='order=2', alpha=0.8)
# plt.xticks([])
# plt.ylabel('Quadratic')
# plt.subplot(4,1,4, sharex=ax)
# librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
#                          y_axis='log')
# plt.tight_layout()
# # plt.show()
# print(p2.shape)
# for i in p2:
#   print(i)
# for i in testItem:
#   print(i.shape)
# print(testItem.shape)
# print(testItem.mean(axis=1))
# print(testItem.mean(axis=0))
