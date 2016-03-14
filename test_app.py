# -*-coding: utf-8 -*-
import os
import unittest

import manage
from app import db


# rv = self.app.get(url, query_string=dict(sort=sort_type))
# rv = self.app.post(url, data=dict())

class UsingDatabase:
    def __init__(self, f):
        self.func = f

    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)
        db.session.rollback()
        print "RollBack after ", self.func.__name__


class LoggingTest:
    def __init__(self, f):
        self.func = f

    def __call__(self):
        self.func()
        print self.func.__name__, " Pass"


class GoJobTestCase(unittest.TestCase):
    def setUp(self):
        manage.app.config['TESTING'] = True
        self.app = manage.app.test_client()

    @classmethod
    def tearDownClass(cls):
        print cls.__name__ + " is Complete.\n"

    def tearDown(self):
        print "  %s Pass" % self._testMethodName


class MainTestCase(GoJobTestCase):

    def test_main_template(self):
        rv = self.app.get('/intro', follow_redirects=True)
        assert "Sunrin Job World" in rv.data

    def test_about_template(self):
        rv = self.app.get('/aboutus')
        assert "About" in rv.data

    def test_main_static(self):
        rv = self.app.get('/css/style.css')
        assert ".default_color{background-color: #2196F3 !important}" in rv.data


class AccountTestCase(GoJobTestCase):
    def test_login_template(self):
        rv = self.app.get('/user/')
        assert "Login" in rv.data


if __name__ == '__main__':
    unittest.main()
