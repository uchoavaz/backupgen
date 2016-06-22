import subprocess
import threading
from zipfile import ZipFile
from glob import glob
from datetime import date
import os
from contextlib import contextmanager
# import sys


@contextmanager
def mounted(remote_dir, local_dir):
    local_dir = os.path.abspath(local_dir)
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

        # echo    g3n0m1k@   |   sudo   -S   mount   -t   cifs
        # '172.16.225.15/genomikalab/Backups/Bancos/' 'temp' -o
        # username=Guest,password=''

    # print "/sbin/mount", "-t", "smbfs", remote_dir, local_dir
    # print("sudo", "-S", "mount", "-t", "cifs", remote_dir,
        #   local_dir, "-o", "username=Guest,password=''")

    # retcode = subprocess.call(["echo", "g3n0m1k@", "|", "sudo", "-S", "mount", "-t", "cifs",
    # remote_dir, local_dir, '-o', "username=Guest,password=''"])
    retcode = subprocess.call(
            " echo g3n0m1k@ | sudo -S mount -t cifs '//172.16.225.15/genomikalab/Backups/Bancos/' 'temp' -o username='genomika',password='g3n3t1c@'", shell=True)
    if retcode != 0:
        raise OSError("mount operation failed")
    try:
        yield
    finally:
        retcode = subprocess.call(["sudo", "umount", local_dir])
        if retcode != 0:
            raise OSError("umount operation failed")


class db_bkp(threading.Thread):

    def __init__(self, id, db):
        self.id = id
        self.db = db
        threading.Thread.__init__(self)

    def run(self):
        print('backup %s' % (self.db))
        command = 'pg_dump -U genomika -w %s > %s.sql' % (self.db, self.db)
        subprocess.call(command, shell=True)


if __name__ == '__main__':
    hostname = subprocess.check_output('hostname', shell=True)
    hostname = hostname.decode('utf-8').strip()
    subprocess.call(
        'echo "localhost:*:*:genomika:g3n3t1c@" > ~/.pgpass', shell=True)
    dbs = subprocess.check_output(
        "psql --list  | cut -f1 -d '|' | tail -n +4", shell=True)
    dbs = dbs.decode('utf-8').split('\n')
    dbs_strip = []
    for i, db in enumerate(dbs):
        if not db:
            continue
        if 'row' in db or 'template' in db:
            continue
        if len(db.strip()) == 0:
            continue
        dbs_strip.append(db.strip())
    dbs = dbs_strip

    th_list = []

    for i, db in enumerate(dbs):
        th_list.append(db_bkp(1, db))

    for th in th_list:
        th.start()
    while len(th_list) > 0:
        for th in th_list:
            if not th.is_alive():
                th_list.remove(th)

    today = str(date.today())

    if not os.path.exists('bkps'):
        os.makedirs('bkps')
    if not os.path.exists('temp'):
        os.makedirs('temp')

    with ZipFile('bkps/' + '%s_%s_pg_bkp.zip' % (hostname, today), 'w') as pg_bkp:
        for bkp in glob('*.sql'):
            pg_bkp.write(bkp)
    subprocess.call('rm *.sql', shell=True)

    folder_destine = r'172.16.225.15/genomikalab/Backups/Bancos/'
    folder_local = 'temp'

    with mounted(folder_destine, folder_local):
        subprocess.call('echo g3n0m1k@ | sudo -S rsync bkps/*.zip %s' %
                        (folder_local), shell=True)
    with mounted(r'172.16.225.15/genomikalab/Backups/Gensoft/', folder_local):
        subprocess.call('echo g3n0m1k@ | sudo -S rsync -r /var/www/genomika-collaboration.gensoft/genomika_soft/media %s' %
                        (folder_local), shell=True)

    # ip_addr = str(input('Digite o ssh de destino(Exemplo: usuario@ip): '))
    # subprocess.call('scp *.zip %s:~/' % (ip_addr), shell=True)
    subprocess.call('rm bkps/*', shell=True)
