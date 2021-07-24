from .mysql_base import DBConnector


class Simple:
    def __init__(self, host, port, user, passwd, database):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database

    def open_sql(self) -> object:
        return DBConnector().get_conn(self.host, self.port, self.user, self.passwd, self.database)

    # insert into 表名 (id,name,sex,age,score) values (data,data,...)
    def insert_data(self, table_name, colum, data):
        """
        :param table_name: 表名(str)
        :param colum: 添加数据的字段的元组 (tuple)
        :param data: 添加的数据的值(tuple)
        :return: -1表示添加失败,0表示重复,大于0表示添加成功的条数
        """
        data_base = ""
        if len(colum) == 1:
            colum_base = colum.__repr__().replace(",", "")
            colum_base = colum_base.replace("'", "")
        else:
            colum_base = colum.__repr__().replace("'", "")
            data_base = data.__repr__().replace('\\', '')
            # data_base = data_base.replace('\'', '')
            # data_base = data_base.replace('\\', '')
            # data_base = data_base.replace('"', '')
        sql = "insert into {} {} values {}".format(table_name, colum_base, data_base)
        # print(sql)
        conn, cur = self.open_sql()
        try:
            cur.execute(sql)
            conn.commit()
            result = cur.rowcount
        except Exception as e:
            result = "-1"
            print(e)
        finally:
            conn.close()
            cur.close()
        return result

    def insert_data_batch(self, table_name, colum, datas):
        """

        :param table_name: 表名(str)
        :param colum: 添加数据的字段的元组 (tuple)
        :param datas: [(),(),(),...] 数据列表 (list)
        :return: -1表示添加失败,0表示重复,大于0表示添加成功的条数
        """
        # insert into 表名 (name,age) values (%s)
        if len(colum) == 1:
            colum_base = colum.__repr__().replace(",", "")
            colum_base = colum_base.replace("'", "")
        else:
            colum_base = colum.__repr__().replace("'", "")

        rep = '('
        for _ in colum:
            rep += "%s,"
        rep = rep[:len(rep) - 1] + ")"
        sql = "insert into " + table_name + " " + colum_base + " values " + rep
        conn, cursor = self.open_sql()
        try:
            cursor.executemany(sql, datas)
            conn.commit()
            result = cursor.rowcount
        except Exception as e:
            result = "-1"
            print(e)
        finally:
            conn.close()
            cursor.close()
        return result

    # delete from student where score<60;
    def delete_data(self, table_name, where=None):
        """
        :param table_name: 表名
        :param where: 删除的约束条件
        :return: -1表示添加失败,0表示重复,大于0表示添加成功的条数
        """
        sql = "delete from {}".format(table_name)
        if where:
            sql += " where {}".format(where)
        conn, cur = self.open_sql()
        try:
            cur.execute(sql)
            conn.commit()
            result = cur.rowcount
        except Exception as e:
            result = "-1"
            print(e)
        finally:
            conn.close()
            cur.close()
        return result

    # update student set key=value,key=value where name="b"
    def update_data(self, table_name, colum, datas, where):
        """

        :param table_name: 表名
        :param colum: 更新了字段元组 (tuple)
        :param datas: 更新字段对应的值
        :param where: 更新的约束条件
        :return: -1表示添加失败,0表示重复,大于0表示添加成功的条数
        """
        sets = ""
        for key, value in zip(colum, datas):
            if isinstance(value, str):
                value = "\"" + value + "\""
            sets += "{}={},".format(key, value)
        sets = sets[:len(sets) - 1]
        sql = "update {} set {} where {}".format(table_name, sets, where)
        conn, cur = self.open_sql()
        try:
            cur.execute(sql)
            conn.commit()
            result = cur.rowcount
        except Exception as e:
            result = "-1"
            print(e)
        finally:
            conn.close()
            cur.close()
        return result

    def query_data(self, table_name, colum, where=None, order_by=None, limit=None, desc=False):
        """

        :param desc: 是否倒序
        :param limit: 个数
        :param order_by: 排序
        :param table_name: 表名 (str)
        :param colum: 查询的列 (tuple或str)
        :param where: 查询的约束条件
        :return: 查询结果
        """
        if "*" != colum:
            if len(colum) == 1:
                colum_base = colum.__repr__().replace(",", "")
                colum_base = colum_base.replace("'", "")
            else:
                colum_base = colum.__repr__().replace("'", "")
                colum_base = colum_base.replace("(", "")
                colum_base = colum_base.replace(")", "")
        else:
            colum_base = colum
        sql = "select {} from {}".format(colum_base, table_name)
        if where:
            where = " where " + where
            sql += where
        if order_by:
            orderby = " order by " + order_by
            sql += orderby
        if desc:
            desc = " desc"
            sql += desc
        if limit:
            limit = " limit " + limit
            sql += limit
        conn, cur = self.open_sql()
        try:
            cur.execute(sql)
            result = cur.fetchall()
        except Exception as e:
            result = "-1"
            print(e)
        finally:
            conn.close()
            cur.close()
        return result
