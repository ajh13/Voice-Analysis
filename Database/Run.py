from Connection import Connect,SFTPConnect,GrabAllFiles,Disconnect
from PrepareTraining import CopyBasedOnGenderToTraining

configPath = 'Database/Dependencies/server.config'
def Main():
    (curs, con) = Connect(configPath)
    (ssh, sftp) = SFTPConnect(configPath)
    GrabAllFiles(sftp, '/mnt/storage/voiceAnalysis/cv-valid-train/')
    CopyBasedOnGenderToTraining(curs)
    Disconnect(con, curs)
    ssh.close()
    sftp.close()
Main()
