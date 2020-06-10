# 开机启动服务
service mysql start
#第一次用管理员帐号创建新用户
sudo mysql -u root -p
create user Admin4ChemForum identified by 'chemistry';
grant all on *.* to 'Admin4ChemForum'@'%';
revoke all on *.* from 'Admin4ChemForum'@'%';
flush privileges;
# 为项目创建数据库
create database ChemForumDataBase;
show databases;
drop database ChemForumDataBase;
mysql -u Admin4ChemForum -p
use ChemForumDataBase;
# 为项目创建用户表、问题表和回答表
create table AnswerInfo (
 ano varchar(128) not null,
 ino varchar(128) not null,
 content text not null,
 email varchar(128) null,
 create_time datetime not null
);
create table IssueInfo (
 ino varchar(128) not null
 primary key,
 email varchar(128) null,
 content text null,
 create_time datetime not null,
 title text not null
);
create table UserInfo (
 email varchar(128) not null
 primary key,
 username varchar(128) charset utf8 default '新用户' not null,
 password varchar(128) not null,
 signature varchar(128) charset utf8 default 'Hello, Chemistry' null,
 create_time datetime null,
 profile_photo varchar(128) default 'default' null,
 last_login_time datetime null,
 level int default 1 not null
);
