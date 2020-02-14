import boto3
import paramiko
from typing import List
import time


pvwa = ""
pvwa_id = ""
test_machine_id = ""
AWS_ACCESS_KEY_ID = "********"
AWS_SECRET_ACCESS_KEY = '********'
SSH_KEY = "/test.pem"
INSTANCE_USER = "********"
TIMEOUT = 60
PORT = 22
REGION_NAME = "********"
TEST_ZIP = "tests.zip"
REMOTE_ZIP_PATH = "/home/ec2-user/tests.zip"
REMOTE_RESULT_PATH = "/home/ec2-user/TestResult.xml"
LOCAL_RESULT_PATH = "/TestResult.xml"
COMMANDS_TEST_MACHINE = [
                        "sudo unzip tests.zip",
                        "sudo mono packages/NUnit.ConsoleRunner.3.10.0/tools/nunit3-console.exe TestAws/bin/Debug/TestAws.dll",
                        ]

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
            print('Running tests')
            stdin, stdout, stderr = ssh.exec_command(command + f" --tp url={pvwa}", timeout=TIMEOUT, get_pty=True)
        else:
            stdin, stdout, stderr = ssh.exec_command(command, timeout=TIMEOUT, get_pty=True)
        output.append((stdin, stdout, stderr))
        print(f'Executed task {command}')
        print(f"command {command} has exit status: {stdout.channel.recv_exit_status()}")
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
    pvwa_instance =  [pvwa for pvwa in pvwa_instances if pvwa.tags[0]['Value'] == 'pvwa'].pop()
    ec2.Instance(pvwa_instance.id).start()
    time_out = time.time() + 60
    print(f'Waiting for instance_id - {pvwa_instance.id}', end='')
    while True:
        print('.', end='')
        if time.time() > time_out:
            break
        try:
            ip = ec2.Instance(pvwa_instance.id).public_ip_address
            if ip and ec2.Instance(pvwa_instance.id).state['Name'] == 'running':
                global pvwa_id
                pvwa_id = pvwa_instance.id
                print(f'PVWA with instance_id - {pvwa_instance.id} and ip - {ip} is ready')
                break
        except Exception:
            continue
    write_file('pvwa', ip)
    global pvwa
    pvwa = ip


def write_file(filename, value):
    with open(f'{filename}.txt', 'a') as file:
        file.write(value)
    print(f'{filename} ip is {value}')


def create_instance():
    instance = ec2.create_instances(
        ImageId='********',
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        SecurityGroupIds=['********', '********'],
        KeyName="test",
        TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': 'test_machine'}, ]}, ]
    ).pop()

    instance_id = instance.id
    time_out = time.time() + 60
    print(f'Waiting for instance_id - {instance_id}', end='')
    while True:
        print('.', end='')
        if time.time() > time_out:
            break
        try:
            ip = ec2.Instance(instance_id).public_ip_address
            if ip and ec2.Instance(instance_id).state['Name'] == 'running':
                time.sleep(40)
                global test_machine_id
                test_machine_id = instance_id
                print(f'Test Machine with instance_id - {instance_id} and ip - {ip} is ready')
                break
        except Exception:
            continue

    write_file('test_machine', ip)
    transfer_ssh(ip, True)
    execute_ssh(COMMANDS_TEST_MACHINE, ip)
    transfer_ssh(ip, False)


def delete_instance(instance_id):
    print(f'Terminating machine with instance_id - {instance_id}')
    ec2.Instance(instance_id).terminate()


def stop_instance(instance_id):
    print(f'Stopping machine with instance_id - {instance_id}')
    ec2.Instance(instance_id).stop()


get_pvwa_address()
create_instance()
delete_instance(test_machine_id)
stop_instance(pvwa_id)
