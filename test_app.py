from flask import url_for
from flask.ext.testing import TestCase

from crawling_job.saramin import *

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
        j = Job('title', 'url', datetime.now())
        db.session.add(j)
        db.session.commit()

        assert j in db.session


class CrawlingTestCase(BaseTestCase):

    def test_get_cnt_major_saramin(self):
        self.assertIsNot(get_cnt_major('major001'), None)

    def test_crawling_saramin(self):
        before_data_cnt = len(Job.query.all())
        saramin_crawling()
        after_data_cnt = len(Job.query.all())

        print "Before = %s\nAfter = %s" % (before_data_cnt, after_data_cnt)

        self.assertGreater(after_data_cnt, before_data_cnt)
