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
fi

cd backupgen

git checkout $backup_genomika_branch

pip3 install -r requirements.txt

if [ "$prod" = 'true']; then
	echo "entrei na copia do env"
	cat .env_prod
	cp .env_prod .env
	cat .env
fi

if [ "$homolog" = 'true']; then
	cp .env_homolog .env
fi

if [ "$migrate" = 'true' ] ; then
        python3 manage.py migrate
fi

if [ "$prod" = 'true']; then
	crontab -r
	/var/www/backupgen/crontab.sh
fi

cron -f &! python3 manage.py runserver 0.0.0.0:$port