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
    for name in filenames:
      if name.endswith(".wav"):
        files.extend(os.path.join(path, name))
  return files
  
def convertWAVtoSpectro(file):
  print("Before %s" % file)
  sample_rate, samples = wavfile.read(file)
  frequencies, times, spectogram = signal.spectrogram(samples, sample_rate)

  plt.pcolormesh(times, frequencies, spectogram)
  plt.ylim((0, 12000))
  plt.xlim((0, .935))
  file = file.split(".wav")[0]
  file += ".png"
  plt.savefig(file)
  print("Converted to Sepctrogram: %s" % file)

def convertAllSpectro():
  all_files = get_files()
  for file in all_files:
    pngFile = file.split(".wav")[0]
    pngFile += ".png"
    if not os.path.isfile(pngFile):
      convertWAVtoSpectro(file)
    else:
      print('Alreaded Converted: %s' % filename)

# def get

# def load_sound_files(files):
#     raw_sounds = []
#     for fp in files:
#         X,sr = librosa.load(fp)
#         raw_sounds.append(X)
#     return raw_sounds

# def plot_waveform(raw_sounds):
#     i = 1
#     fig = plt.figure(figsize=(25, 60))
#     title = 'test'
#     fig.suptitle("Waveform " + title, fontsize=12)
#     for f in raw_sounds:
#         plt.subplot(14, 1, i)
#         librosa.display.waveplot(np.array(f), sr=22050)
#         i += 1
#     plt.show()

convertAllSpectro()
