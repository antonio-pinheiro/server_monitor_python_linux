import os

SECRET_KEY = 'server_key'
MYSQL_HOST = "192.168.3.127"
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"
MYSQL_DB = "server_monitor"
MYSQL_PORT = 3306
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
