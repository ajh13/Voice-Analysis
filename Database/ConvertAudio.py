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

def convertAllSpectro():
  cwd = os.getcwd()
  abspath = os.path.abspath(__file__)
  dname = os.path.dirname(abspath)
  os.chdir(dname)
  all_files = []
  all_files = get_files()
  for file in all_files:
    if ".wav" in file:
      pngFile = file.split(".wav")[0]
      pngFile += ".png"
    else:
      pngFile = file
    if not os.path.isfile(pngFile):
      convertWAVtoSpectro(file)
    else:
      print('Alreaded Converted: %s' % file)
  os.chdir(cwd)
