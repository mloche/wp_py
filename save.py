mysqldump --user=wordpres --password=password --databases wordpress > /tmp/wp.dump
mysql -u wordpress --password=password < /tmp/wp.dump
dumps mysql db ?

