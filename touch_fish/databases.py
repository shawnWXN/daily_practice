import importlib
import time
from DBUtils.PooledDB import PooledDB
from functools import wraps


def timeit(func):
    """ Decorator to calc the time cost
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print('[{}] costs [{}]secs'.format(func.__name__, end_time - start_time))
        return result

    return wrapper


class DataBase(object):

    def __init__(self, db_type, config):

        self.__db_type = db_type

        if self.__db_type == 'mysql':
            db_creator = importlib.import_module('MySQLdb')
        elif self.__db_type == 'sqlserver':
            db_creator = importlib.import_module('pymssql')
        elif self.__db_type == 'oracle':
            db_creator = importlib.import_module('cx_Oracle')
        else:
            raise Exception('unsupported database type ' + self.__db_type)
        self.pool = PooledDB(
            creator=db_creator,
            mincached=0,
            maxcached=6,
            maxconnections=0,
            maxshared=3,
            maxusage=0,
            blocking=True,
            ping=0,
            **config
        )

    @timeit
    def execute_query(self, sql, as_dict=True):
        conn = None
        cur = None
        try:
            conn = self.pool.connection()
            cur = conn.cursor()
            cur.execute(sql)
            rst = cur.fetchall()
            if rst:
                if as_dict:
                    fields = [tup[0] for tup in cur._cursor.description]
                    return [dict(zip(fields, row)) for row in rst]
                return rst
            return rst

        except Exception as e:
            print('[{}]meet error'.format(sql))
            print(e.args[-1])
            return ()
        finally:
            if conn:
                conn.close()
            if cur:
                cur.close()

    def execute_many(self, sql, data):
        """
        一种指令但多组数据的sql语句执行函数
        :param sql:
        :param data:
        :return:
        """
        db = None
        cursor = None
        try:
            db = self.pool.connection()
            cursor = db.cursor()
            cursor.executemany(sql, data)
            db.commit()
            return True
        except Exception as e:
            print('[{}]meet error'.format(sql))
            print(e.args[-1])
            db.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()


MySQL = DataBase(
    'mysql', {'user': 'root', 'host': 'localhost', 'password': 'wang2702', 'database': 'sakila', 'port': 3306}
)
MsSQL = DataBase(
    'sqlserver', {'user': 'sa', 'host': '10.167.219.229', 'password': 'Wstg168!!!', 'database': 'FOCTestRecord2019', 'port':3000}
)
Oracle = DataBase(
    'oracle', {'user': 'NSDSFC', 'dsn': '10.132.37.80:1903/pcas', 'password': 'NSGSFC'}
)
