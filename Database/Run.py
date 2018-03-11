from Connection import Connect,SFTPConnect,GrabAllFiles,Disconnect,ListTables
from PrepareTraining import CopyBasedOnGenderToTraining

configPath = 'Database/Dependencies/server.config'
def Main():
    (curs, con) = Connect(configPath)
    (ssh, sftp) = SFTPConnect(configPath)
    ListTables(curs)
    GrabAllFiles(sftp, '/mnt/storage/voiceAnalysis/')
    CopyBasedOnGenderToTraining(curs)
    Disconnect(con, curs)
    ssh.close()
    sftp.close()
Main()
