import base
from base import Base
import sys
import paramiko


class Transfer(Base):
    instance_ip = sys.argv[1]
    transfer_up = sys.argv[2]
    print(f"instance_ip - {instance_ip}")
    print(f"transfer_up - {transfer_up}")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(instance_ip, port=base.PORT, username=base.INSTANCE_USER, key_filename=base.SSH_KEY,
                banner_timeout=base.TIMEOUT, timeout=base.TIMEOUT, auth_timeout=base.TIMEOUT)
    print(f'connected to {instance_ip}')

    if transfer_up is not "0":
        print(f'Upload file - {base.TEST_ZIP} to remote machine')
        ftp_client = ssh.open_sftp()
        ftp_client.put(base.TEST_ZIP, base.REMOTE_ZIP_PATH)
        ftp_client.close()
    else:
        print(f'Download file - {base.REMOTE_RESULT_PATH} from remote machine')
        ftp_client = ssh.open_sftp()
        ftp_client.get(base.REMOTE_RESULT_PATH, base.LOCAL_RESULT_PATH)
        ftp_client.close()
