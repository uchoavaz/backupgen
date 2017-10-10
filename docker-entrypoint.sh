
#!/bin/bash
/usr/sbin/sshd -D &! 

echo "listen_addresses = '*'" >> /etc/postgresql/9.6/main/postgresql.conf
service postgresql restart

cd /var/www
git clone git@gitlab.com:genomika/backupy.git
cd backupy

git checkout $backupy_branch

cd ..
cd backupgen

git checkout $backup_genomika_branch

cp /var/www/backupgen/.env /var/www/backupgen/

pip3 install -r requirements.txt

if [ "$migrate" = true ] ; then
        python3 manage.py migrate
fi

/var/www/backupgen/crontab.sh

cron -f &! python3 manage.py runserver 0.0.0.0:$port