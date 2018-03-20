from Connection import Connect,SFTPConnect,GrabAllFiles,Disconnect,ListTables,GrabFile
from PrepareTraining import CopyBasedOnGenderToTraining, CopyBasedOnColumn

configPath = 'Dependencies/server.config'

def Main():
    (curs, con) = Connect(configPath)
    (ssh, sftp) = SFTPConnect(configPath)
    ListTables(curs)
    # GrabAllFiles(sftp, '/mnt/storage/voiceAnalysis/')
    # CopyBasedOnGenderToTraining(curs,sftp)
    CopyBasedOnColumn(curs,sftp,'gender')
    Disconnect(con, curs)
    ssh.close()
    sftp.close()
Main()
