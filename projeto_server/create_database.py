import mysql.connector

connect = mysql.connector.connect(
    host="192.168.3.127",
    user="root",
    password="123456"
)

cursor = connect.cursor()

cursor.execute('create database if not exists server_monitor')
cursor.execute('use server_monitor')
cursor.execute("""create table if not exists server(
                id int(30) not null auto_increment,
                name varchar(50) collate utf8_bin not null,
                ip_address varchar(15) not null,
                category varchar(40) collate utf8_bin not null,
                primary key (id)
                )engine=innodb default charset=utf8 collate=utf8_bin"""
               )
cursor.execute("""create table if not exists user (
                id varchar(30) primary key not null,
                name varchar(20) not null,
                password varchar(8) not null
                )"""
               )

cursor.executemany(
    'INSERT INTO server_monitor.user (id, name, password) VALUES (%s, %s, %s)',
    [
        ('Administrator', 'Antônio Pinheiro', '@123@'),
    ])

cursor.execute('select * from server_monitor.user')
print(' -------------  Users:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
cursor.executemany(
    'INSERT INTO server_monitor.server (name, ip_address, category) VALUES (%s, %s, %s)',
    [
        ('Debian Samba','192.168.50.50', 'File Server'),
        ('Debian MySQL','192.168.51.51', 'MySQL Server'),
    ])

cursor.execute('select * from server_monitor.server')
print(' -------------  Servers:  -------------')
for server in cursor.fetchall():
    print(server[1])

connect.commit()
cursor.close()