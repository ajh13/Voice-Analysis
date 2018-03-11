from Connection import Connect, ListTables, Disconnect, GrabFile
import os

configPath = 'Dependencies/server.config'

'''
Function: Copies files to Male and Female folders based on database gender column.
Args:     Cursor connection created from connection.py
Return:   Copies files from Files/cv-valid-train and place into Training/female or Training/male
Notes:    Need to download all cv-valid-train files before running this function
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


# def Main():
#     (cursor, con) = Connect(configPath)
#     CopyFilesToProperFolders(cursor)
#     Disconnect(con, cursor)
# Main()
