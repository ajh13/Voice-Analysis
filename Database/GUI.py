from tkinter import filedialog
from tkinter import *


a_path = "Selected Path..."


def getPath(root, path):
    global a_path
    root.filename = filedialog.askopenfilename(initialdir="C:/Users/Taylor/Documents/GitHub/Voice-Analysis/Audio", title="Select file",
                                               filetypes=(("WAV files", "*.wav"), ("all files", "*.*")))
    path = Label(main, text=root.filename, relief="sunken")
    path.grid(row=0, column=1, sticky=NSEW, padx=2, pady=3)
    main.update()
    a_path = root.filename
    
# Function to return comparison between recording and model
def compare():

    
# Function to report and update file information to training data column
def fileInfo():



main = Tk()
main.title("Who's There?")
main.configure(background='grey')
main.geometry("1000x610")
main.minsize(1000, 610)

# Initialize Main containers layout

# Initialize top frame widgets
# Top frame widget layout
pathl = Label(main, text="*.WAV File Path:", relief="raised")
path = Label(main, text=a_path, relief="sunken")
pathb = Button(main, text=". . .", command=lambda: getPath(main, path))
pathl.grid(row=0, column=0, sticky=NSEW, padx=1, pady=1)
path.grid(row=0, column=1, sticky=NSEW, padx=2, pady=3)
pathb.grid(row=0, column=2, sticky=NSEW, padx=3, pady=5)

l2 = Label(main, text="list relevant data here...", relief="sunken")
l2.grid(row=1, column=0, sticky=NSEW, padx=1, pady=1)

# Initialize bottom frame widgets
# Bottom frame widget layout
B1 = Button(main, text="Run Analysis")
B1.grid(row=2, column=0, sticky=NSEW, padx=40, pady=40)

l8 = Label(main, text="Model")
l8.grid(row=1, column=1, columnspan=2, sticky=N)

l9 = Label(main, text="Results", relief="sunken")
l9.grid(row=2, column=1, columnspan=2, sticky=NSEW, padx=2, pady=2)

main.grid_rowconfigure(0, weight=10)
main.grid_rowconfigure(1, weight=500)
main.grid_rowconfigure(2, weight=100)

main.grid_columnconfigure(0, weight=300)
main.grid_columnconfigure(1, weight=660)
main.grid_columnconfigure(2, weight=40)



main.mainloop()

"""

"""