#!/bin/bash
echo "starting script"
apt install apache2 mariadb-server gnupg lsb-release apt-transport-https ca-certificates
wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg
echo "packages installed, adding  php 7.4 sources"
echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/php.list
apt update
apt install php7.4 php7.4-mysql
echo "PHP 7.4 installed, installing WP CLI tool"
wget -O /tmp/wp-cli.phar https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
chmod +x /tmp/wp-cli.phar
mv /tmp/wp-cli.phar /usr/local/bin/wp
wp cli update
echo "creating DB"
mysql < wp.sql
chown -R www-data:www-data /var/www/html
mv /var/www/html/index.html /var/www/html/index.html.old
cd /var/www/html
echo "installing WP"
sudo -u www-data wp core download
sudo -u www-data wp core config --dbname=wordpress --dbuser=wordpress --dbpass=wordpress
sudo -u www-data wp core install --url=http://10.0.2.15 --title=title --admin_user=admin --admin_password=password --admin_email=email@local.net
echo "script ended"
