import pymysql
from pymysql.err import DatabaseError

from search.utils.tools import singleton


@singleton
class DBConnector:
    def get_conn(self, host, port, user, passwd, database):
        try:
            conn = pymysql.connect(host=host, port=port, passwd=passwd, user=user, database=database)
            cursor = conn.cursor()
        except Exception as e:
            raise DatabaseError("Connect Error") from e
        return conn, cursor
