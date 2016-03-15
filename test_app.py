# -*-coding: utf-8 -*-

from flask import url_for
from flask.ext.testing import TestCase

from crawling_job.saramin import *

from app.fb_manager import get_user_school, check_sunrin

from app.models import Job
from manage import app


class BaseTestCase(TestCase):
    def create_app(self):
        app.config['SECRET_KEY'] = 'development-test-key'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # + join(test_cwd, 'flask-tracking.db')

        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TemplateTestCase(BaseTestCase):
    render_templates = False

    def test_job_template(self):
        self.client.get(url_for('job.job_list'))
        self.assertTemplateUsed('job/worklist.html')

    def test_index_template(self):
        self.client.get(url_for('main.index'))
        self.assertTemplateUsed('main/index.html')

    def test_about_template(self):
        self.client.get(url_for('main.about'))
        self.assertTemplateUsed('main/about.html')

    def test_login_template(self):
        self.client.get(url_for('user.login_template'))

        self.assertTemplateUsed('account/login.html')

    def test_static_files(self):
        response = self.client.get(url_for('main.static_css', filename='style.css'))
        self.assert200(response, 'Static Error!')


class ModelingTestCase(BaseTestCase):
    def test_User_Model(self):
        u = User('name', 'userid', 'userpw', 'fb_id', 'fb_accesstoken')
        db.session.add(u)
        db.session.commit()

        assert u in db.session

    def test_Company_Model(self):
        c = Company('name')
        db.session.add(c)
        db.session.commit()

        assert c in db.session

    def test_Job_Model(self):
        j = Job('title', '1000', 'seoul', 'only weeks', 'major001', datetime.now(), 'url')
        db.session.add(j)
        db.session.commit()

        assert j in db.session


"""
class CrawlingTestCase(BaseTestCase):
    def test_get_cnt_major_saramin(self):
        self.assertIsNot(get_cnt_major('major001'), None)

    def test_crawling_saramin(self):
        before_data_cnt = len(Job.query.all())
        saramin_crawling()
        after_data_cnt = len(Job.query.all())

        print "Before = %s\nAfter = %s" % (before_data_cnt, after_data_cnt)

        self.assertGreater(after_data_cnt, before_data_cnt)
"""


class FacebookTestCase(BaseTestCase):
    def test_get_user_school(self):
        access_token = "CAADkT44ofvABALXGeDxOUqnmsUK7BQW8uZBoEHZBKYXZADNyEZB6FPAItZCjCkgsw6pNXA1ZAtLrw1WZBZBF4Xpmd2KK" \
                       "xdiDZC5qaByd0k0XbiyEmyQFeHopnyXe66uFipVvvHm8OkrCWX0Xh2IWNZBb63NObZAG33EHib4XZAKs2ZCV3MgEU9jO0" \
                       "LeQMFGmCZCoK6v3wZD"

        school_name = get_user_school(access_token)

        self.assertNotEqual(school_name, None)

    def test_check_sunrin(self):
        result = check_sunrin(u'Sunrin High School')

        self.assertEqual(result, True)

        result = check_sunrin(u'선린인터넷고등학교')

        self.assertEqual(result, True)

        result = check_sunrin(u'알파고등학교')

        self.assertEqual(result, False)

        result = check_sunrin(u'SunRin High School')

        self.assertEqual(result, True)

        result = check_sunrin(u'Super High School')

        self.assertEqual(result, False)