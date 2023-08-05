# coding=utf-8
# pylint: disable=wrong-import-position, relative-import, import-error
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
from resources.benchmark_db_resource import BenchmarkDBResource
from resources.env_db_resource import EnvDBResource


class DBClient(object):

    def __init__(self):
        self.benchmark_resource = BenchmarkDBResource(db_name="performance_test")
        self.env_resource = EnvDBResource(db_name="nodes")
