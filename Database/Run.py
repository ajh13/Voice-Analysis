try:
  from Database import Connection
except:
  import Connection
try:
  from Database import PrepareTraining
except:
  import PrepareTraining

configPath = 'Dependencies/server.config'

def Main():
    (curs, con) = Connection.Connect(configPath)
    (ssh, sftp) = Connection.SFTPConnect(configPath)
    Connection.ListTables(curs)
    # GrabAllFiles(sftp, '/mnt/storage/voiceAnalysis/')
    # CopyBasedOnGenderToTraining(curs,sftp)
    PrepareTraining.CopyBasedOnColumn(curs,sftp,'gender')
    Connection.Disconnect(con, curs)
    ssh.close()
    sftp.close()
