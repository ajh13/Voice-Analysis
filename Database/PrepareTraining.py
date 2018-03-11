from Connection import Connect, ListTables, Disconnect
from shutil import copyfile
import os

configPath = 'Dependencies/server.config'

'''
Function: Copies files to Male and Female folders based on database gender column.
Args:     Cursor connection created from connection.py
Return:   Copies files from Files/cv-valid-train and place into Training/female or Training/male
Notes:    Need to download all cv-valid-train files before running this function
'''

def CopyBasedOnGenderToTraining(cursor):
    # Copy male data to Training/male
    cursor.execute("SELECT filename FROM trainingdata WHERE gender = 'male'")
    row = cursor.fetchall()
    for item in row:
        for filename in item:
            location = 'Files/' + filename
            filename = filename.replace('cv-valid-train/', '')
            newLocation = 'Training/male/' + filename
            if not os.path.exists('Training/male/'):
                os.makedirs('Training/male/')
            copyfile(location,newLocation)
            print(filename)
    # Copy female data to Training/female
    cursor.execute("SELECT filename FROM trainingdata WHERE gender = 'female'")
    row = cursor.fetchall()
    for item in row:
        for filename in item:
            location = 'Files/' + filename
            filename = filename.replace('cv-valid-train/', '')
            newLocation = 'Training/female/' + filename
            if not os.path.exists('Training/female/'):
                os.makedirs('Training/female/')
            copyfile(location,newLocation)
            print(filename)


# def Main():
#     (cursor, con) = Connect(configPath)
#     CopyFilesToProperFolders(cursor)
#     Disconnect(con, cursor)
# Main()
