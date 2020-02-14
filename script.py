import boto3
import paramiko
from typing import List
import time


AWS_ACCESS_KEY_ID = "******"
AWS_SECRET_ACCESS_KEY = "******"
SSH_KEY = "/test.pem"
INSTANCE_USER = "ec2-user"
TIMEOUT = 60
PORT = 22
REGION_NAME = "us-east-1"
TEST_ZIP = "C:/Program Files (x86)/Jenkins/workspace/TestAws_master/tests.zip"
REMOTE_ZIP_PATH = "/home/ec2-user/tests.zip"
REMOTE_RESULT_PATH = "/home/ec2-user/TestResult.xml"
LOCAL_RESULT_PATH = "C:/Program Files (x86)/Jenkins/workspace/TestAws_master/TestResult.xml"
COMMANDS_TEST_MACHINE = [
                        "sudo unzip tests.zip",
                        "sudo mono packages/NUnit.ConsoleRunner.3.10.0/tools/nunit3-console.exe TestAws/bin/Debug/TestAws.dll",
                        ]
pvwa = ""

s = boto3.Session(region_name=REGION_NAME, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
ec2 = s.resource('ec2')
instances = ec2.instances.all()


def execute_ssh(tasks, instance_ip) -> List[tuple]:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(instance_ip, port=PORT, username=INSTANCE_USER, key_filename=SSH_KEY, banner_timeout=TIMEOUT,
                timeout=TIMEOUT, auth_timeout=TIMEOUT)
    output = []
    print(f'connected to {instance_ip}')
    for command in tasks:
        if "mono" in command:
            stdin, stdout, stderr = ssh.exec_command(command + f" --tp url={pvwa}", timeout=TIMEOUT, get_pty=True)
        else:
            stdin, stdout, stderr = ssh.exec_command(command, timeout=TIMEOUT, get_pty=True)

        output.append((stdin, stdout, stderr))
        print(f'Executed task {command}')
        print(f"command {command} has exit status: {stdout.channel.recv_exit_status()}")
        print(stdout)
        stdin.flush()
    return output


def transfer_ssh(instance_ip, transfer_up):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(instance_ip, port=PORT, username=INSTANCE_USER, key_filename=SSH_KEY, banner_timeout=TIMEOUT,
                timeout=TIMEOUT, auth_timeout=TIMEOUT)
    print(f'connected to {instance_ip}')

    if transfer_up:
        print(f'Upload file - {TEST_ZIP} to remote machine')
        ftp_client = ssh.open_sftp()
        ftp_client.put(TEST_ZIP, REMOTE_ZIP_PATH)
        ftp_client.close()
    else:
        print(f'Download file - {REMOTE_RESULT_PATH} from remote machine')
        ftp_client = ssh.open_sftp()
        ftp_client.get(REMOTE_RESULT_PATH, LOCAL_RESULT_PATH)
        ftp_client.close()


def get_pvwa_address():
    pvwa_instances = [i for i in instances]
    pvwa_instance = [pvwa.public_ip_address for pvwa in pvwa_instances if pvwa.state['Name'] == 'running' and pvwa.tags[0]['Value'] == 'pvwa'].pop()
    write_file('pvwa', pvwa_instance)
    global pvwa
    pvwa = pvwa_instance


def write_file(filename, value):
    with open(f'{filename}.txt', 'a') as file:
        file.write(value)
    print(f'{filename} ip is {value}')


def create_instance():
    instance = ec2.create_instances(
        ImageId='ami-0677611d5bf124658',
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        SecurityGroupIds=['******', '******'],
        KeyName="test",
        TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': 'test_machine'}, ]}, ]
    ).pop()

    instance_id = instance.id
    time_out = time.time() + 60
    while True:
        print(f'Waiting for instance_id - {instance_id}...')
        if time.time() > time_out:
            break
        try:
            ip = ec2.Instance(instance_id).public_ip_address
            if ip and ec2.Instance(instance_id).state['Name'] == 'running':
                time.sleep(40)
                print(f'Test Machine with instance_id - {instance_id} and ip - {ip} is ready')
                break
        except Exception:
            continue

    write_file('test_machine', ip)
    transfer_ssh(ip, True)
    execute_ssh(COMMANDS_TEST_MACHINE, ip)
    transfer_ssh(ip, False)


get_pvwa_address()
create_instance()
