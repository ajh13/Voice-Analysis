from ConvertAudio import convertWAVtoSpectro
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
from GenerateModel import TestModel
import os
import csv
import time
a_path = "Browse..."
output = "Results"


def browse(source, pathLabel, imgPanel):
    global a_path
    source.filename = filedialog.askopenfilename(initialdir="C:/Voice-Analysis/Audio",
                                                 title="Select file",
                                                 filetypes=(("WAV files", "*.wav"), ("all files", "*.*")))
    a_path = source.filename

    # update path label
    pathLabel = Label(main, text=source.filename, relief="sunken")
    pathLabel.grid(row=0, column=1, sticky=NSEW, padx=2, pady=3)

    # update file info
    fileInfo()

    # update spectrogram
    updateSpec(a_path, imgPanel)



# Function to report and update file information to training data column
def fileInfo():
    #put text= features dictionary of input .wav
    features ={}
    featuretext=""
    # with open('C:/Voice-Analysis/Audio/Features.csv', mode='r') as infile:
       #  reader = csv.reader(infile)
       #  features = {rows[0]:rows[1] for rows in reader}
    with open('C:/Voice-Analysis/Audio/Features.csv') as f:
        records = csv.DictReader(f)
        for row in records:
            print(row)
            for keys in row:
                featuretext += keys + ': ' + row[keys] + '\n'
            # featuretext += row + '\n' 
    # for keys in features:
    #       featuretext += keys + " : " + features[keys] + "\n"
    fileinfo = Label(main, text=featuretext, relief="sunken")
    fileinfo.grid(row=1, column=0, sticky=NSEW, padx=1, pady=1)


# Update spectrogram, still need to pull file
def updateSpec(file, imgPanel):
    convertWAVtoSpectro(file)
    file = file.split(".wav")[0]
    file += ".png"
    while not os.path.isfile(file):
        time.sleep(1)
    print(file)
    img = ImageTk.PhotoImage(Image.open(file))
    imgPanel.configure(image=img)
    imgPanel.image = img
    imgPanel.grid(row=1, column=1, columnspan=2, sticky=N+EW, padx=5, pady=2)
    main.update()
    


# Function to return comparison between recording and model
def updateResults():
    global output
    global a_path
    pred = TestModel("C:/Voice-Analysis/Audio/Features.csv")
    print("Female: " , pred[0] , " Male: " , pred[1])
    output = "Female: " , pred[0] , " Male: " , pred[1]
    results = Label(main, text=output, relief="sunken")
    results.grid(row=2, column=1, columnspan=2, sticky=NSEW, padx=2, pady=2)

    main.update()


# Initialize Window
main = Tk()
main.title("Who's There?")
main.configure(background='grey')
main.geometry("1000x610")
main.minsize(1000, 610)

# Initialize top frame widgets
# Top frame widget layout
# Put default image here
img = ImageTk.PhotoImage(Image.open("D:/Documents/Voice-Analysis/Images/Default.png"))
imgPanel = Label(main, image=img)
imgPanel.grid(row=1, column=1, columnspan=2, sticky=N+EW, padx=5, pady=2)
pathHeader = Label(main, text="*.WAV File Path:", relief="raised")
path = Label(main, text=a_path, relief="sunken")
getPath = Button(main, text=". . .", command=lambda: browse(main, path, imgPanel))
getPath.configure(background="light grey")

# Path Layout
pathHeader.grid(row=0, column=0, sticky=NSEW, padx=1, pady=1)
path.grid(row=0, column=1, sticky=NSEW, padx=2, pady=3)
getPath.grid(row=0, column=2, sticky=NSEW, padx=3, pady=5)

fileinfo = Label(main, text="list relevant data here...", relief="sunken")
fileinfo.grid(row=1, column=0, sticky=NSEW, padx=1, pady=1)

# Initialize bottom frame widgets
# Bottom frame widget layout
runButton = Button(main, text="Run Analysis", command=updateResults, relief="raised")
runButton.configure(background="light grey")
runButton.grid(row=2, column=0, sticky=NSEW, padx=40, pady=40)


results = Label(main, text=output, relief="sunken")
results.grid(row=2, column=1, columnspan=2, sticky=NSEW, padx=2, pady=2)

main.grid_rowconfigure(0, weight=10)
main.grid_rowconfigure(1, weight=500)
main.grid_rowconfigure(2, weight=100)

main.grid_columnconfigure(0, weight=300)
main.grid_columnconfigure(1, weight=660)
main.grid_columnconfigure(2, weight=40)

main.mainloop()

"""

"""