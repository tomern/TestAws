import base
import time
from base import Base


class StartSutMachine(Base):
    pvwa_instances = [i for i in base.Base.instances]
    pvwa_instance = [pvwa for pvwa in pvwa_instances if pvwa.tags[0]['Value'] == 'pvwa'].pop()
    base.Base.ec2.Instance(pvwa_instance.id).start()
    time_out = time.time() + 60
    print(f'Waiting for instance_id - {pvwa_instance.id}', end='')
    while True:
        print('.', end='')
        if time.time() > time_out:
            break
        try:
            ip = base.Base.ec2.Instance(pvwa_instance.id).public_ip_address
            if ip and base.Base.ec2.Instance(pvwa_instance.id).state['Name'] == 'running':
                print(f'PVWA with instance_id - {pvwa_instance.id} and ip - {ip} is ready')
                break
        except Exception:
            continue
    base.Base.write_file('pvwa_ip', ip)
    base.Base.write_file('pvwa_id', pvwa_instance.id)

