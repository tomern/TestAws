import boto3

pvwa = ""
pvwa_id = ""
test_machine_id = ""
AWS_ACCESS_KEY_ID = "*****"
AWS_SECRET_ACCESS_KEY = '*****'
SSH_KEY = "C:/test.pem"
INSTANCE_USER = "*****"
TIMEOUT = 60
PORT = 22
REGION_NAME = "*****"
TEST_ZIP = "C:/tests.zip"
REMOTE_ZIP_PATH = "/home/tests.zip"
REMOTE_RESULT_PATH = "/home/TestResult.xml"
LOCAL_RESULT_PATH = "C:/TestResult.xml"
COMMANDS_TEST_MACHINE = [
    "sudo unzip tests.zip",
    "sudo mono packages/NUnit.ConsoleRunner.3.10.0/tools/nunit3-console.exe TestAws/bin/Debug/TestAws.dll",
]


class Base:
    s = boto3.Session(region_name=REGION_NAME, aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    ec2 = s.resource('ec2')
    instances = ec2.instances.all()

    def write_file(filename, value):
        with open(f'{filename}.txt', 'a') as file:
            file.write(value)
        print(f'{filename} - {value}')


