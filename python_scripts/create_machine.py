import base
import time
from base import Base


class CreateMachine(Base):
    instance = base.Base.ec2.create_instances(
        ImageId='*****',
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        SecurityGroupIds=['*****', '*****'],
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
            ip = base.Base.ec2.Instance(instance_id).public_ip_address
            if ip and base.Base.ec2.Instance(instance_id).state['Name'] == 'running':
                time.sleep(40)
                print(f'Test Machine with instance_id - {instance_id} and ip - {ip} is ready')
                break
        except Exception:
            continue

    base.Base.write_file('test_machine_ip', ip)
    base.Base.write_file('test_machine_id', instance_id)


