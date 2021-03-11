create database wordpress;
create user 'wordpress'@'localhost' identified by 'wordpress';
grant all on wordpress.* to 'wordpress'@'localhost' identified by 'wordpress' with grant option;
flush privileges;
