import sys
from base import Base


class StopInstance(Base):
    instance_id = sys.argv[1]
    print(f'Stopping machine with instance_id - {instance_id}')
    Base.ec2.Instance(instance_id).stop()
