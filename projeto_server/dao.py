from models import Server, User

SQL_DELETE_SERVER = 'delete from server where id = %s'
SQL_SERVER_BY_ID = 'SELECT id, name, ip_address, category from server where id = %s'
SQL_USER_BY_ID = 'SELECT id, name, password from user where id = %s'
SQL_UPDATE_SERVER = 'UPDATE server SET name=%s, ip_address=%s, category=%s where id = %s'
SQL_SEARCH_SERVERS = 'SELECT id, name, ip_address, category from server'
SQL_CREATE_SERVER = 'INSERT into server (name, ip_address, category) values (%s, %s, %s)'


class ServerDao:
    def __init__(self, db):
        self.__db = db

    def save(self, server):
        cursor = self.__db.connection.cursor()

        if (server.id):
            cursor.execute(SQL_UPDATE_SERVER, (server.name, server.ip_address, server.category, server.id))
        else:
            cursor.execute(SQL_CREATE_SERVER, (server.name, server.ip_address, server.category))
            server.id = cursor.lastrowid
        self.__db.connection.commit()
        return server

    def list(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_SEARCH_SERVERS)
        servers = create_server(cursor.fetchall())
        return servers

    def search_by_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_SERVER_BY_ID, (id,))
        tupla = cursor.fetchone()
        return Server(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def delete(self, id):
        self.__db.connection.cursor().execute(SQL_DELETE_SERVER, (id, ))
        self.__db.connection.commit()


class UserDao:
    def __init__(self, db):
        self.__db = db

    def search_by_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USER_BY_ID, (id,))
        data = cursor.fetchone()
        user = create_user(data) if data else None
        return user

def create_server(servers):
    def create_server_with_tuple(tupla):
        return Server(tupla[1], tupla[2], tupla[3], id=tupla[0])
    return list(map(create_server_with_tuple, servers))


def create_user(tupla):
    return User(tupla[0], tupla[1], tupla[2])
