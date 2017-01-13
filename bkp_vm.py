
import subprocess
from decouple import config


class VirtualMachineBkp():

    commands = {
        'vms_list': 'xe vm-list'
    }

    def __init__(self):
        self.mount_path = config('MOUNT_PATH')

    def get_vms_json(self):
        vms_list = subprocess.Popen(
            self.commands['vms_list'],
            shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE).stdout.readlines()

        if vms_list == []:
            raise Exception('0 Virtual Machines Found !')

        for vm in vms_list:
            pass

    def backup(self):
        try:
            self.get_vms_list()
        except Exception as e:
            import ipdb;ipdb.set_trace()
