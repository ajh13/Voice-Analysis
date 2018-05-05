# GETTING DATA FROM R3.5.0
import os
import wave
import contextlib
import pandas as pd
import rpy2
import rpy2.robjects.packages as rpackages
import rpy2.robjects as robjects
base = rpackages.importr('base')
utils = rpackages.importr('utils')
warble = rpackages.importr('warbleR')
utils.chooseCRANmirror(ind=1)
packnames = ('warbleR')
utils.install_packages(packnames)

# pi = robjects.r['pi']
# col_names = ['sound.files','sel', 'start', 'end']
# #data_frame_create = robjects.r['testdata <- data.frame(1,1,1)']
# data_frame = robjects.DataFrame({})
# wl = 512
# threshold = 15
# parallel = 1
# fast = True
# path = 'C:/Users/alexa/PycharmProjects/Voice-Analysis/Database/test'
# filenames = ['sample-000003.wav']
# # bp var in specan function
# freq_lim = robjects.IntVector([0,28])
# # X var in specan function
# X = {col_names[0]: robjects.StrVector(filenames), col_names[1]: robjects.IntVector([1])\
# 	,col_names[2]: robjects.FloatVector([0]), col_names[3]: robjects.FloatVector([2.0]) }
# warble.specan(X,\
# 	freq_lim, \
# 	wl, \
# 	threshold, parallel,\
# 	 fast,\
# 	  path)
# dataf = robjects.DataFrame(d)
# print(dataf)

# Get list of all filenames in female and male folders
# Get length of each filename 0:dur
# write filename, selec, 0, dur to csv
# Plug in R code using generated csv
def get_files(foldername):
  files = []
  for (path, dirnames, filenames) in os.walk(foldername):
    files.extend(os.path.join(path, name) for name in filenames)
  return files

def convert_wav_to_csv(gender):
	# Converts wav folder to csv
	# genders = ["male", "female"]
	output_file_name = 'test/DFOutput' + gender + '.csv'
	selec = 1
	start = 0
	data = {'sound.files' : [], 'selec' : [],'start' : [], 'end' : []}
	filenames = get_files("test\\" + gender)
	for file in filenames:
		dur = 0
		with contextlib.closing(wave.open(file,'r')) as f:
		      frames = f.getnframes()
		      rate = f.getframerate()
		      dur = frames / float(rate)
		data['sound.files'].append(file.split("\\")[2])
		data['selec'].append(selec)
		data['start'].append(start)
		data['end'].append(dur)
	df = pd.DataFrame(data=data)
	df.to_csv(output_file_name, index=False, columns=["sound.files", "selec", "start", "end"])
	return output_file_name
	# Takes generated csv as input for

def r_simulate(csv_string, single_input_location = "Holder"):
	base_location = os.getcwd() + "\\"
	DFO_location = base_location + csv_string
	temp_dict = {'row_names' : 'row.names'}
	ignore_cols = ["Unnamed: 0", "sound.files", "selec", "duration", "time.median", "time.Q25", "time.Q75", "time.IQR", "time.ent", "entropy", "startdom", "enddom", "dfslope", "meanpeakf"]
	dataf = robjects.DataFrame.from_csvfile(DFO_location)
	if "female" in csv_string:
		workDirectory = base_location + "test/female"
	elif "male" in csv_string:
		workDirectory = base_location + "test/male"
	else:
		workDirectory = single_input_location
	robjects.r['setwd'](workDirectory)
	# robjects.r('setwd("C:/Users/alexa/PycharmProjects/Voice-Analysis/Database/test/male")')
	cwd = robjects.r('getwd()')
	print("Working directory: " , cwd)
	unfiltered_df = warble.specan(dataf)
	base_location += "Features2.csv"
	robjects.r['write.csv'](unfiltered_df,file=base_location)
	filtered_df = pd.read_csv(base_location)
	filtered_df = filtered_df.drop(ignore_cols, axis=1)
	if "female" in csv_string:
		filtered_df['label'] = "female"
	elif "male" in csv_string:
		filtered_df['label'] = "male"
	filtered_df.to_csv(base_location, index=False)

r_simulate(convert_wav_to_csv("female"))
# r_simulate(convert_wav_to_csv("female"))
