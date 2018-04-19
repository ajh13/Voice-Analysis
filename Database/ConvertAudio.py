from pydub import AudioSegment
import os
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import tensorflow as tf
import librosa
import librosa.display
import numpy as np

# For converting to wav
def dumpWAV( name ):
  filename = os.path.splitext(name)[0] + '.wav'
  AudioSegment.from_file(name).export(filename, format='wav')
  os.remove(name)

def get_files():
  files = []
  for (path, dirnames, filenames) in os.walk('Training'):
    files.extend(os.path.join(path, name) for name in filenames)
  return files
  
def convertWAVtoSpectro(file):
  sample_rate, samples = wavfile.read(file)
  frequencies, times, spectogram = signal.spectrogram(samples, sample_rate)

  plt.pcolormesh(times, frequencies, spectogram)
  plt.ylim((0, 12000))
  plt.xlim((.5, 3))
  file = file.split(".wav")[0]
  file += ".png"
  plt.savefig(file)
  print("Converted to Sepctrogram: %s" % file)

def convertWAVtoWAVE(file):
  samples, sr = librosa.load(file)
  fig = plt.figure(figsize=(25,60), dpi = 900)
  n,f = zip(sex,samples):
  plt.subplot(10,1,1)
  librosa.display.waveplot(np.array(f),sr=22050)
  plt.title(n.title())
  plt.suptitle('Figure 1: Waveplot',x=0.5, y=0.915,fontsize=18)
  plt.show()
  #file = file.split(".wav")[0]
  #ile += ".png"
  #plt.savefig(file)
  #print("Converted to Waveplot: %s" % file)

def convertAllSpectro():
  cwd = os.getcwd()
  abspath = os.path.abspath(__file__)
  dname = os.path.dirname(abspath)
  os.chdir(dname)
  all_files = []
  all_files = get_files()
  for file in all_files:
    if ".wav" in file:
   	  convertWAVtoWAVE(file)
      pngFile = file.split(".wav")[0]
      pngFile += ".png"
    else:
      pngFile = file
    if not os.path.isfile(pngFile):
      convertWAVtoSpectro(file)
    else:
      print('Already Converted: %s' % file)
  os.chdir(cwd)

#
def extract_feature(file_name):
  X, sample_rate = librosa.load(file_name)
  stft = np.abs(librosa.stft(X))
  mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)
  chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
  mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
  contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)
  tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T,axis=0)
  return mfccs,chroma,mel,contrast,tonnetz

def parse_audio_files(parent_dir,sub_dirs,file_ext='*.wav'):
  features, labels = np.empty((0,193)), np.empty(0)
  for label, sub_dir in enumerate(sub_dirs):
    for fn in glob.glob(os.path.join(parent_dir, sub_dir, file_ext)):
      mfccs, chroma, mel, contrast,tonnetz = extract_feature(fn)
      ext_features = np.hstack([mfccs,chroma,mel,contrast,tonnetz])
      features = np.vstack([features,ext_features])
      labels = np.append(labels, fn.split('/')[2].split('-')[1])
  return np.array(features), np.array(labels, dtype = np.int)

#gender label encoding
def gender_encode(labels):
  n_labels = len(labels)
  n_unique_labels = len(np.unique(labels))
  gender_encode = np.zeros((n_labels,n_unique_labels))
  gender_encode[np.arange(n_labels), labels] = 1
  return gender_encode