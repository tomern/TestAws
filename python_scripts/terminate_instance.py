import sys
from base import Base


class TerminateInstance(Base):
    instance_id = sys.argv[1]
    print(f'Terminating machine with instance_id - {instance_id}')
    Base.ec2.Instance(instance_id).terminate()
