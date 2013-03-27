apt-get install -y libapache2-mod-wsgi python-jinja2 python-markdown python-mysqldb mysql-server
mysql -u root -p <<EOF
create database if not exists tp_db;
grant all privileges on tp_db.* to tp_user@localhost identified by 'tp123321';
EOF
