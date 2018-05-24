#!/bin/bash

case $ip_db_client in
    '172.16.225.11'|'producao.genomika.com')

echo "Production db denied"

;;
    *)

echo "listen_addresses = '*'" >> /etc/postgresql/9.6/main/postgresql.conf
service postgresql restart

PGPASSWORD=$pgpassword_server pg_dump -h $ip_db_server -p $port_db_server -U $user_db_server -F c -b -v -f "/var/www/gensoft.sql" $namedb_db_server

PGPASSWORD=$pgpassword_client dropdb -h $ip_db_client -p $port_db_client -U $user_db_client $namedb_db_client

PGPASSWORD=$pgpassword_client createdb -h $ip_db_client -p $port_db_client -U $user_db_client $namedb_db_client

PGPASSWORD=$pgpassword_client pg_restore -U $user_db_client -h $ip_db_client -p $port_db_client -d $namedb_db_client < /var/www/gensoft.sql

;;
esac