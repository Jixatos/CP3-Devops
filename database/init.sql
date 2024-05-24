create user 'bd_user'@'localhost' IDENTIFIED BY '@cp3devops'
grant all on bdcp3.* TO 'bd_user'@'localhost';
flush privileges;
create database bdcp3;
use bdcp3;
create table tbl_cadastro ( id generated always as identity int , username varchar(255), password varchar(255) );