#-*- coding: utf-8 -*-

'''

Our script for full backup of current vms to any storage using mount syntax.

author: marcel@genomika.com.br;  Marcel Caraciolo
'''

import subprocess
import optparse
import os
import time

log_path = '/home/backup/vm_backup.log'


class CalledProcessError(Exception):
    """This exception is raised when a process run by check_call() or
        check_output() returns a non-zero exit status.
        The exit status will be stored in the returncode attribute;
        check_output() will also store the output in the output attribute.
    """
    def __init__(self, returncode, cmd, output=None):
        self.returncode = returncode
        self.cmd = cmd
        self.output = output

    def __str__(self):
        return "Command '%s' returned non-zero exit status %d" % (self.cmd, self.returncode)


class VM(object):
    def __init__(self, uuid, name, status):
        self.uuid = uuid
        self.name = name
        self.status = status

    def __str__(self):
        return '%s - %s (%s)' % (self.uuid, self.name, self.status)

    def export(self, directory_name=None):
        start = time.time()
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())

        file_name = '%s %s.xva' % (timestamp, self.name)
        if directory_name is not None:
            file_name = os.path.join(directory_name, file_name)

        # create a snapshot
        snapshot_uuid = check_output(['xe', 'vm-snapshot', 'uuid=' + self.uuid,
                                      'new-name-label=backup-' + self.name]).strip()

        # change some params so that the snapshot can be exported
        cmd = "xe template-param-set is-a-template=false ha-always-run=false uuid=" + snapshot_uuid
        check_output(cmd, shell=True)

        # export snapshot
        cmd = 'xe vm-export vm=%s filename="%s" --compress' % (snapshot_uuid, file_name)
        check_output(['xe', 'vm-export', 'vm=' + snapshot_uuid,
                      'filename=' + file_name, '--compress'])

        # remove old snapshot again
        cmd = "xe vm-uninstall uuid=%s force=true" % snapshot_uuid
        check_output(cmd, shell=True)
        print('Exported VM "%s" in %s seconds.' % (self.name, time.time() - start))

def check_output(command, shell=False):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=shell)
    output, unused_err = p.communicate()
    retcode = p.poll()
    if retcode:
        raise CalledProcessError(retcode, command, output=output)
    return output

def audit(dbtool):
    pass

def get_backup_vms():
    cmd = "xe vm-list is-control-domain=false is-a-snapshot=false"
    output = check_output(cmd, shell=True)
    result = []
    for vm in output.split("\n\n\n"):
        lines = vm.splitlines()
        if lines:
            uuid = lines[0].split(":")[1][1:]
            name = lines[1].split(":")[1][1:]
            status = lines[2].split(":")[1][1:]
            result.append(VM(uuid, name, status))
    return result

def export_all_vms(device, directory, delete_old):
    #1. First let's check if the device is mounted.
    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        check_output(['mountpoint', '-q', directory])
    except CalledProcessError:
        check_output(['mount', device, directory])

    #2. Let's take a look at the history and do the cleanup.

    #3.Let's get the metadata information

    #3.1 Auditlog from XenServer

    #3.2 Pool metadata backup

    #4.Checking all Running Vm's and doing our job: backup!

    #5. If everything goes well, ok, otherwise send email with alert!
    pass

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-d', '--delete-old', action="store_true", default=False)
    parser.add_option('-i', '--dir', action="store", dest="directory")
    parser.add_option('-o', '--device', action="store", dest="device")

    options, remainder = parser.parse_args()
    if options.directory and options.device:
        export_all_vms(options.device, options.directory, options.delete_old)
    else:
        print('No device and no directory found')

