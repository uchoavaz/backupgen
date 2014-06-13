#-*- coding: utf-8 -*-

'''

Our script for full backup of current vms to any storage using mount syntax.

author: marcel@genomika.com.br;  Marcel Caraciolo
'''

import subprocess
import optparse
import os
import time
import logging

log_path = '/home/backup/vm_backup.log'

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    filename=log_path,
                    filemode='w')

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

        logging.info('Exported Snapshot from VM "%s" in %s seconds.' % (self.name, time.time() - start))

def check_output(command, shell=False):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=shell)
    output, unused_err = p.communicate()
    retcode = p.poll()
    if retcode:
        raise CalledProcessError(retcode, command, output=output)
    return output

def parse_timestamp(timestamp):
    pass

def cleanup(directory, snapshots, copies=3):
    '''
    Cleans it up so
    that we only have the last copies value backups on it.
    '''

    #for each directory you must find only the backups for a specific VM.

    #remove now the oldest vms
    current_snapshots = get_snapshots()


    #for each directory you must find only the snapshots for a specific VM.
    machines = {}
    backup_vms = get_backup_vms()
    for snap in current_snapshots:
        for vm in backup_vms:
            if vm.name in snap[1]:
                machines.setdefault(vm.name, [])
                machines[vm.name].append(snap, parse_timestamp(snap))

    #sort the machines from the latest to the oldest.
    remove_vms = []

    for vm in machines:
        machines[vm] =  sorted(machines[vm], key = lambda t: -t)
        #remove only the oldest 3 and only if we have more than n copies.
        if len(machines[vm]) > copies:
            remove_vms.extend(machines[vm][copies:])

    #remove now the oldest vms
    for snap, time in remove_vms:
        cmd = "xe vm-uninstall uuid=%s force=true" % snap[0]
        check_output(cmd, shell=True)
    return remove_vms


def get_snapshots():
    cmd = 'xe snapshot-list'
    output = check_output(cmd, shell=True)
    result = []
    for snap in output.split('\n\n\n'):
        lines = snap.splitlines()
        if lines:
            uuid = lines[0].split(":")[1][1:]
            name = lines[1].split(":")[1][1:]
            result.append((uuid, name))

    return result

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


def export_all_vms(directory, delete_old):
    #1. First let's check if the device is mounted.
    logging.info('===Starting snapshots backup routine===')
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info('Done, folder %s created.' % directory)

    #2.Checking all Running Vm's and doing our job: backup!
    vms = get_backup_vms()
    failures = []
    snapshots = []
    for vm in vms:
        try:
            snapshot = vm.export(directory)
            snapshots.append(snapshot)
        except CalledProcessError:
            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
            failures.append((vm.name, timestamp))
    if failures:
        content = "VM   Time Failure\n"
        for failure in failures:
            content += '%s  %s\n' % (failure[0], failure[1])
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
        send_mail('[FAILURE] Problems on Exporting Vms - %s' % timestamp, content)

    #4. Let's take a look at the history and do the cleanup.
    if delete_old:
        try:
            cleanup(directory, snapshots)
            logging.info('Done, cleanup.')
        except CalledProcessError:
            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
            send_mail('[FAILURE] Delete Old Problems - %s' % timestamp , 'Problems running backup Delete old files at %s' % timestamp)

    #6. Store all the info into the database, why ?  For future web monitor.

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-d', '--delete-old', action="store_true", default=False)
    parser.add_option('-i', '--dir', action="store", dest="directory")

    options, remainder = parser.parse_args()
    if options.directory:
        export_all_vms(options.directory, options.delete_old)
    else:
        print('No device and no directory found')

