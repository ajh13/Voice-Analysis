from pydub import AudioSegment
import os
def dumpWAV( name ):
  filename = os.path.splitext(name)[0] + '.wav'
  AudioSegment.from_file(name).export(filename, format='wav')
  os.remove(name)