mysql -u root -p <<EOF
create database if not exists tp_db;
grant all privileges on tp_db.* to tp_user@localhost identified by 'tp123321';
EOF
