from Connection import Connect, ListTables, Disconnect, GrabFile
import csv

configPath = 'Dependencies/server.config'

def InsertFromCSV(cursor, conn, filePath):
    with open(filePath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sqlStatement = "SELECT filename FROM trainingdata WHERE filename = '" + row['filename'] + "'"
            cursor.execute(sqlStatement)
            sql = cursor.fetchone()
            if sql is None:
                sqlText = row['text']
                sqlText = sqlText.replace("'","")
                sqlInsert = "INSERT INTO trainingdata VALUES (%s, '%s', '%s', '%s', %s, '%s', '%s');" %\
                    (row['up_votes'],sqlText,row['gender'],row['filename'],row['down_votes'],row['age'],row['accent'])
                sqlInsert = sqlInsert.replace("''","NULL")
                print(sqlInsert)
                cursor.execute(sqlInsert)
                conn.commit()

def Main():
    (curs, con) = Connect(configPath)
    InsertFromCSV(curs,con,'Files/cv-valid-train.csv')
    Disconnect(con,curs)
Main()