# coding=utf-8
# pylint: disable=import-error, broad-except
from resources.models.database import SqlConnection


class TestDBResource(object):

    def __init__(self, db_name="production_test"):
        self.sql = SqlConnection(db_name=db_name)

    def get_result(self, key):
        cmd = "SELECT * FROM test_results WHERE test_key='{}'".format(key)
        self.sql.cursor.execute(cmd)
        result = self.sql.cursor.fetchone()
        return result