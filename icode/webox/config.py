


class Config(object):

    class db(object):
        host = "feng-dev"
        port = 3306
        user = "test"
        passwd = "test"
        database = "yonder"
        charset = "utf8mb4"

    class yonder(object):
        host = "feng-dev"
        port = 8020

    @classmethod
    def db_conn_str(cls):
        # mysql+pymysql://scott:tiger@localhost/foo?charset=utf8mb4
        s = "mysql+pymysql://{u}:{p}@{h}:{port}/{db}?charset={c}".format(
            u=cls.db.user, p=cls.db.passwd, 
            h=cls.db.host, port=cls.db.port, 
            db=cls.db.database, c=cls.db.charset
        )
        return s

    class local(object):
        name = "local"
        host = "127.0.0.1"
        port = 22
        user = "feng"
        passwd = "123"

    class vmc1(object):
        name = "vmc1"
        host = "172.18.0.2"
        port = 22
        user = "root"
        passwd = "r123"
