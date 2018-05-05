# from pydub import AudioSegment
import os
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
# import tensorflow as tf
# import librosa
# import librosa.display
import numpy as np
import wave
import contextlib


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
  dur = 0
  with contextlib.closing(wave.open(file,'r')) as f:
      frames = f.getnframes()
      rate = f.getframerate()
      dur = frames / float(rate)
  plt.pcolormesh(times, frequencies, spectogram)
  plt.ylim((0, 2800))
  plt.xlim((0, dur))
  file = file.split(".wav")[0]
  file += ".png"
  plt.savefig(file)
  print("Converted to Sepctrogram: %s" % file)

# def convertWAVtoWAVE(sex, file):
#   samples, sr = librosa.load(file)
#   fig = plt.figure(figsize=(25,60), dpi = 900)
#   n,f = zip(sex,samples):
#   plt.subplot(10,1,1)
#   librosa.display.waveplot(np.array(f),sr=22050)
#   plt.title(n.title())
#   plt.suptitle('Figure 1: Waveplot',x=0.5, y=0.915,fontsize=18)
#   plt.show()
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
      pngFile = file.split(".wav")[0]
      pngFile += ".png"
    else:
      pngFile = file
    if not os.path.isfile(pngFile):
      convertWAVtoSpectro(file)
    else:
      print('Already Converted: %s' % file)
  os.chdir(cwd)
