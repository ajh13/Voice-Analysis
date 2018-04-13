import pydub
import os
def dumpWAV( name ):
  filename = os.path.splitext(name)[0] + '.wav'
  pydub.AudioSegment.from_file(name).export(filename, format='wav')
  os.remove(name)

