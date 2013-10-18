echo $0
INSTALL_DIR=$(dirname "$0")
echo $INSTALL_DIR

apt-get install -y apache2 libapache2-mod-wsgi python-jinja2 python-markdown python-mysql.connector mysql-server python-memcache coffeescript node-less ruby-haml node-uglify python-imaging ttf-dejavu-core
cp $INSTALL_DIR/apache_etc /etc/apache2/sites-available/default
service apache2 restart
