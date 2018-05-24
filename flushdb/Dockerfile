FROM dockerregistry.genomika.com/ubuntu-genomika:14.04

#Commands backupy
WORKDIR /var/www

RUN apt-get update -y
RUN apt install libpq-dev python-dev -y
RUN apt-get -y install python-pip
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
RUN wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | sudo apt-key add -
RUN apt-get update -y
RUN apt-get install postgresql postgresql-contrib -y
RUN echo "listen_addresses = '*'" >> /etc/postgresql/9.6/main/postgresql.conf
RUN service postgresql restart
