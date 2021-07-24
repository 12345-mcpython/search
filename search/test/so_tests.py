import unittest

import requests

from search.config.config import Config
from search.database.mysql import Simple


class SoTest(unittest.TestCase):
    def setUp(self):
        self.db = Simple(Config.MYSQL['MYSQL_HOST'], Config.MYSQL["MYSQL_PORT"], Config.MYSQL['MYSQL_USER'],
                         Config.MYSQL['MYSQL_PASSWORD'], "so")
        self.data = [["mc官网", "http://mc.com"], ["mc论坛", "http://mcluntan.com"]]
        for i in self.data:
            self.db.insert_data("test", ("title", "url"), tuple(i))

    def test_so_index_is_loading(self):
        r = requests.get("http://127.0.0.1:5000")
        self.assertIn("Mc", r.text)
        self.assertIn("Mc一下", r.text)
        req = requests.get("http://127.0.0.1:5000/search?q=mc")
        for i in self.data:
            self.assertIn(i[0], req.text)
            self.assertIn(i[1], req.text)
    def tearDown(self):
        self.db.delete_data("test")