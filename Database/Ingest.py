import csv

configPath = 'Dependencies/server.config'

def InsertFromCSVCheckForDuplicate(cursor, conn, filePath):
    i = 0
    with open(filePath) as csvfile:
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

def InsertFromCSVFRESH(cursor, conn, filePath):
    i = 0
    with open(filePath) as csvfile:
        sqlInsert = ""
        reader = csv.DictReader(csvfile)
        for row in reader:
            sqlText = row['text']
            sqlText = sqlText.replace("'", "")
            sqlInsert += "INSERT INTO trainingdata VALUES (%s, '%s', '%s', '%s', %s, '%s', '%s');" % \
                        (row['up_votes'], sqlText, row['gender'], row['filename'], row['down_votes'], row['age'],
                        row['accent'])
            i += 1
        print(sqlInsert)
        sqlInsert = sqlInsert.replace("''", "NULL")
        cursor.execute(sqlInsert)
        conn.commit()

# def Main():
#     (curs, con) = Connect(configPath)
#     InsertFromCSV(curs,con,'Files/cv-valid-train.csv')
#     Disconnect(con,curs)
# Main()