from Connection import Connect, ListTables, Disconnect, GrabFile
import os
import re

configPath = 'Dependencies/server.config'

'''
Function: Copies files to Male and Female folders based on database gender column.
Args:     Cursor connection created from connection.py
Return:   Copies files from Files/cv-valid-train and place into Training/female or Training/male
'''

def CopyBasedOnGenderToTraining(cursor,sftp):
    if not os.path.exists('Training/female/'):
        os.makedirs('Training/female/')
    if not os.path.exists('Training/male/'):
        os.makedirs('Training/male/')
    # Copy male data to Training/male
    cursor.execute("SELECT filename FROM trainingdata WHERE gender = 'male'")
    row = cursor.fetchall()
    for item in row:
        for filename in item:
            filename = filename.replace('cv-valid-train/', '')
            GrabFile(sftp,filename,'/mnt/storage/voiceAnalysis/cv-valid-train/','Training/male/')
    # Copy female data to Training/female
    cursor.execute("SELECT filename FROM trainingdata WHERE gender = 'female'")
    row = cursor.fetchall()
    for item in row:
        for filename in item:
            filename = filename.replace('cv-valid-train/', '')
            GrabFile(sftp,filename,'/mnt/storage/voiceAnalysis/cv-valid-train/','Training/female/')

'''
Function: Copies mp3 files to folders based on all types specified in the column arg
Args:     Cursor connection created from connection.py
          sftp connection created from connection.py
          column in the database you want to organize the files by
Return:   Copies files from Files/cv-valid-train and place into Training folder with sub folders
'''

def CopyBasedOnColumn(cursor,sftp,column):
    sqlStatement = "SELECT " + column + " FROM trainingdata GROUP BY " + column
    cursor.execute(sqlStatement)
    columnItems = cursor.fetchall()
    regex = re.compile('[^a-zA-Z]')
    for item in columnItems:
        itemName = regex.sub('',str(item))
        if itemName != 'None' and itemName != 'other':
            filePath = 'Training/' + itemName + '/'
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            sqlStatement = "SELECT filename FROM trainingdata WHERE gender = '" + itemName + "'"
            cursor.execute(sqlStatement)
            row = cursor.fetchall()
            for file in row:
                for filename in file:
                    filename = filename.replace('cv-valid-train/', '')
                    localPath = 'Training/' + itemName + '/'
                    GrabFile(sftp,filename,'/mnt/storage/voiceAnalysis/cv-valid-train/',localPath)