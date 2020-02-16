import base
from base import Base
import sys
import paramiko


class Execute(Base):
    instance_ip = sys.argv[1]
    tp_url = sys.argv[2]
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(instance_ip, port=base.PORT, username=base.INSTANCE_USER, key_filename=base.SSH_KEY, banner_timeout=base.TIMEOUT,
                timeout=base.TIMEOUT, auth_timeout=base.TIMEOUT)
    output = []
    print(f'connected to {instance_ip}')
    for command in base.COMMANDS_TEST_MACHINE:
        if "mono" in command:
            print('Running tests')
            stdin, stdout, stderr = ssh.exec_command(command + f" --tp url={tp_url}", timeout=base.TIMEOUT, get_pty=True)
        else:
            stdin, stdout, stderr = ssh.exec_command(command, timeout=base.TIMEOUT, get_pty=True)
        output.append((stdin, stdout, stderr))
        print(f'Executed task {command}')
        print(f"command {command} has exit status: {stdout.channel.recv_exit_status()}")
        stdin.flush()

