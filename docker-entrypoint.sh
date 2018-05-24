#!/bin/bash
/usr/sbin/sshd -D &! 

echo "listen_addresses = '*'" >> /etc/postgresql/9.6/main/postgresql.conf
service postgresql restart

cd /var/www

if [ "$prod" = 'true' ]; then
	git clone git@gitlab.com:genomika/backupy.git
	cd backupy

	git checkout $backupy_branch
	cd ..
	cd backupgen

	git checkout $backup_genomika_branch
	cp .env_prod .env
	crontab -r
	/var/www/backupgen/crontab.sh
fi

if [ "$homolog" = 'true']; then
	cd backupgen
	cp .env_homolog .env
	git checkout $backup_genomika_branch
	cp .env_homolog .env
fi

pip3 install -r requirements.txt

if [ "$migrate" = 'true' ] ; then
        python3 manage.py migrate
fi

cron -f &! python3 manage.py runserver 0.0.0.0:$port