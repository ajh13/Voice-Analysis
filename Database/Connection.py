import xml.etree.ElementTree as ET
from ..Dependencies.Database import psycopg2


configPath = '../Dependencies/Database/server.config'
'''
Function: Reads server config file and converts xml to dictionary
Args:
          @filename: string path leading to server.config file
Return:   containing the keys 'address', 'username', 
          'password'(optional)
'''
def GetCredentials(filename):
  credentials = {}
  tree = ET.parse(filename)
  root = tree.getroot()
  for child in root:
    credentials[child.tag] = child.text
  return credentials


'''
Function: Opens connection to database using credentials passed to function
          and creates a cursor objeect to be used to execute db operations
Args:     
          @filename: string path leading to server.config file
Return:   cursor psycopg2 object (Used to perform database operations) 
'''
def Connect(filename):
  credentials = GetCredentials(filename)
  try:
    conn = psycopg2.connect(dbname=credentials['dbname'],
      user=credentials['username'],
      password=credentials['password'],
      host=credentials['host'])
    cur = conn.cursor()
  except:
    print('Couldn\'t connect to server: ', credentials['host'])
    exit() 
  return (cur, conn)


'''
Function: Closes connection and cursor instances to db
Args:     None
Return:   Boolean on whether or not both cursor and connection were
          successfully closed
'''
def Disconnect(connection, cursor):
  success = True
  if(connection):
    connection.close()
    print("Closing connection.")
  else:
    success = False
    print("[Warning] Could not close connection. No connection to db found.")
  if(cursor):
    cursor.close()
    print("Closing cursor.")
  else:
    success = False
    print("[Warning] Could not close cursor. No cursor found.\n")
  return success
  
def ListTables(cursor):
	cur.execute("SELECT * FROM pg_catalog.pg_tables;")

def Main():
  (curs, con)=Connect(configPath)
  ListTables(curs)
  Disconnect(con,curs)
Main()