#-*- coding: utf-8 -*-

'''

Our script for full backup of current vms to any storage using mount syntax.

author: marcel@genomika.com.br;  Marcel Caraciolo
'''

import subprocess
import optparse
import os
import time
import glob

log_path = '/home/backup/vm_backup.log'

remote = {'dbtool': 'dbtool'}

def send_mail(subject, content):
    check_output(['cat', '/root/mailheader.txt', '>', '/root/message.tmp'], shell=True)
    check_output(['echo', 'Subject: ' + subject, '>>', '/root/message.tmp'], shell=True)
    check_output(['echo', content, '>>', '/root/message.tmp'], shell=True)
    check_output(['ssmtp', 'marcel@genomika.com.br', '<', '/root/message.tmp'], shell=True)
    check_output(['rm', '-f', '/root/message.tmp'], shell=True)

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

def audit(dbtool, directory):
    '''
    A plaintext dump of all the info needed to figure out what used to be connected
    to what and where it used to live, all the SR, VM, VIF, UUID's etc.
    are here in a reasonably readable format if needed.
    '''
    output_file  =  os.path.join(directory, 'auditlog-xenshuttle.txt')
    check_output([dbtool, '-a', '/var/xapi/state.db', '>', output_file])

def parse_timestamp(timestamp):
    pass

def cleanup(device, directory, vms, copies=3):
    '''
    unmounts and remounts the backup disk, and then cleans it up so
    that we only have the last copies value backups on it.
    '''

    #unmount and the mount again procedure.
    check_output(['umount', directory])

    check_output(['mount', device, directory])

    #for each directory you must find only the backups for a specific VM.
    machines = {}
    for vm in vms:
        for xva in glob.glob(directory + '/*.xva'):
            if vm.name in xva:
                machines.setdefault(vm.name, [])
                machines[vm.name].append(xva, parse_timestamp(xva))

    #sort the machines from the latest to the oldest.
    remove_vms = []

    for vm in machines:
        machines[vm] =  sorted(machines[vm], key = lambda t: -t)
        #remove only the oldest 3 and only if we have more than n copies.
        if len(machines[vm]) > copies:
            remove_vms.extend(machines[vm][copies:])

    #remove now the oldest vms
    for vm in remove_vms:
        os.remove(os.path.join(directory, vm))

    return remove_vms

def metadata_backup(directory, host):
    '''
    Backs up the metadata of the Xen Pool in a restorable format.
    Backs up the host machines over to the backup drive as well.
    '''
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
    backup_name = 'xenshuttle-metadata-%s.bak'  %  timestamp
    output = os.path.join(directory, backup_name)
    check_output(['xe pool-dump-database', 'file-name=', output], shell=True)


    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
    backup_name = 'xenshuttle-host-backup-%s.bak'  %  timestamp
    output = os.path.join(directory, backup_name)
    check_output(['xe host-backup', 'file-name=', output, 'host=', host], shell=True)

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

    #2.1 Auditlog from XenServer
    try:
        audit(remote['dbtool'], directory)
    except CalledProcessError:
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
        send_mail('[FAILURE] Backup AuditLog - %s' % timestamp , 'Problems running backup Auditlog at %s' % timestamp)

    #2.2 Pool metadata backup
    try:
        metadata_backup(directory, remote['host'])
    except CalledProcessError:
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
        send_mail('[FAILURE] Backup MetaData Pool - %s' % timestamp , 'Problems running backup MetaDataBackup at %s' % timestamp)

    #3.Checking all Running Vm's and doing our job: backup!
    vms = get_backup_vms()
    for vm in vms:
        vm.export(directory)

    #4. Let's take a look at the history and do the cleanup.
    if delete_old:
        try:
            cleanup(device, directory, vms)
        except CalledProcessError:
            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
            send_mail('[FAILURE] Delete Old Problems - %s' % timestamp , 'Problems running backup Delete old files at %s' % timestamp)

    #6. Store all the info into the database, why ?  For future web monitor.

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

