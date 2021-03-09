#!/bin/bash

apt install apache2 mariadb-server gnupg lsb-release apt-transport-https ca-certificates
wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg
echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" | sudo tee /etc/apt/source.list.d/php.list
apt update
apt install php7.4 php7.4-mysql
wget -O /tmp/wp-cli.phar https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
chmod +x /tmp/wp-cli.phar
mv /tmp/wp-cli.phar /usr/local/bin/wp
wp cli update
mkdir -p /var/www/html/
chown -R www-data:www-data /var/www/html
cd /var/www/html
sudo -u www-data wp core download
