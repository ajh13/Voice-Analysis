import xml.etree.ElementTree as ET
import psycopg2
import paramiko
import os
from ConvertAudio import dumpWAV
from stat import S_ISDIR

configPath = 'Dependencies/server.config'

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
Function: Connects to the SSH server
Args:
          @filename: string path leading to server.config file
Return:   sshClient object and sftp object
Note:     Make sure to close the connections
'''
def SFTPConnect(filename):
    credents = GetCredentials(filename)
    host = credents['host']
    user = credents['sshUser']
    password = credents['sshPass']

    sshClient = paramiko.SSHClient()
    sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshClient.load_system_host_keys()
    sshClient.connect(host, 22, user, password)
    sftp = sshClient.open_sftp()

    print("Created SFTP to %s server" % host)

    return sshClient, sftp


'''
Function: Downloads a file to the local system in Files directory
Args:
          filename: string path leading to file in the SSH server
          sftp: sftp object from ssh object
Return:   Downloads file to Files/filename
'''
def GrabFile(sftp,filename,remotepath,localpath):
    localpath += filename
    remotepath += filename
    wavFile = localpath[:-4] + '.wav'
    mp3File = localpath[:-4] + '.mp3'
    if not os.path.exists('Files'):
        os.makedirs('Files')
    if not os.path.isfile(mp3File) and not os.path.isfile(wavFile):
        sftp.get(remotepath, localpath)
        print('Downloaded %s to %s' % (filename, localpath))
        # Convert to wav
        dumpWAV(localpath)
        print('Converted %s to .wav format' % (localpath))
    else:
        print('Already Downloaded File: %s' % filename)


'''
Function: Recursively downloads all files that haven't been downloaded already
          (will not update files)
Args:
          sftp: sftp object from ssh object
          remotepath: path that you want to download
Return:   Downloads all remotepath files to Files/
'''
def GrabAllFiles (sftp, remotepath):
  if not os.path.exists("Files"):
    os.makedirs("Files")
  files = []
  folders = []
  for f in sftp.listdir_attr(remotepath):
    if S_ISDIR(f.st_mode):
      folders.append(f.filename)
    else:
      files.append(f.filename)
      path = remotepath
      path += f.filename
      localpath = path
      localpath = localpath.replace("/mnt/storage/voiceAnalysis/", "Files/")
      if not os.path.isfile(localpath):
        sftp.get(path, localpath)
        print('Downloaded %s' % localpath)
      else:
        print('File already downloaded: %s' % localpath)

  for folder in folders:
      new_path= remotepath + folder + '/'
      localpath = 'Files/' + folder
      if not os.path.exists(localpath):
        os.makedirs(localpath)
      GrabAllFiles(sftp, new_path)


'''
Function: Opens connection to database using credentials passed to function
          and creates a cursor object to be used to execute db operations
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
        print('Successfully connected to:', credentials['host'])
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
    if (connection):
        connection.close()
        print("Closing connection.")
    else:
        success = False
        print("[Warning] Could not close connection. No connection to db found.")
    if (cursor):
        cursor.close()
        print("Closing cursor.")
    else:
        success = False
        print("[Warning] Could not close cursor. No cursor found.\n")
    return success


def ListTables(cursor):
    cursor.execute('SELECT * FROM pg_tables WHERE pg_tables.schemaname = \'public\';')
    res = cursor.fetchall()
    i = 1
    print('schemaname\ttablename\ttableowner\ttablespace\thasindexes\thasrules\thastriggers\trowsecurity')
    for table in res:
        print(i, '. ', end='')
        for attr in table:
            print(attr, end='\t')
        i += 1
        print('')