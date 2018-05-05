# from ConvertAudio import convertWAVtoSpectro
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

a_path = "Browse..."
output = "Results"


def browse(source, pathLabel):
    global a_path
    source.filename = filedialog.askopenfilename(initialdir="C:/Users/Taylor/Documents/GitHub/Voice-Analysis/Audio",
                                                 title="Select file",
                                                 filetypes=(("WAV files", "*.wav"), ("all files", "*.*")))
    a_path = source.filename

    # update path label
    pathLabel = Label(main, text=source.filename, relief="sunken")
    pathLabel.grid(row=0, column=1, sticky=NSEW, padx=2, pady=3)

    # update file info
    fileInfo()

    # update spectrogram
    updateSpec()

    main.update()


# Function to report and update file information to training data column
def fileInfo():
    fileinfo = Label(main, text="INSERT STRING FROM CSV HERE", relief="sunken")
    fileinfo.grid(row=1, column=0, sticky=NSEW, padx=1, pady=1)


# Update spectrogram, still need to pull file
def updateSpec(file):
    #convertWAVtoSpectro(file)
    file = file.split(".wav")[0]
    file += ".png"
    print(file)


# Function to return comparison between recording and model
def updateResults():
    global output
    output = "WIP"
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
pathHeader = Label(main, text="*.WAV File Path:", relief="raised")
path = Label(main, text=a_path, relief="sunken")
getPath = Button(main, text=". . .", command=lambda: browse(main, path))
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

# Put default image here
img = ImageTk.PhotoImage(Image.open("C:/Users/Taylor/Documents/GitHub/Voice-Analysis/Images/Default.png"))
imgPanel = Label(main, image=img)
imgPanel.grid(row=1, column=1, columnspan=2, sticky=N+EW, padx=5, pady=2)

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