
Steps to setup database using MariaDB/MySQL
================

SQL commands
-----------
create database comtrade;
create user 'CMARCINIAK'@'localhost' identified by 'ifpri360';
grant all privileges on comtrade.* to 'CMARCINIAK'@'localhost';
alter database comtrade character set utf8mb4 collate utf8mb4_unicode_ci;

Run comtrade_schema.py