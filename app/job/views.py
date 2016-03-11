#!/usr/bin/env python
# -*- coding:utf-8 -*-
from BeautifulSoup import BeautifulSoup
from flask import render_template, redirect, url_for
from selenium import webdriver
from sqlalchemy.exc import IntegrityError

from . import job_blueprint
from ..models import *

browser = webdriver.PhantomJS()


@job_blueprint.route('/')
def job_list():
    all_job = Job.query.all()
    return render_template('job/worklist.html',
                           all_job=all_job)


def add_job_data_db(title, company, url, end, role=None):
    c = Company(company)

    db.session.add(c)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        c = Company.query.filter_by(name=company).first()

    j = Job(title, url, end, role)
    c.job.append(j)

    db.session.add(j)

    db.session.commit()


@job_blueprint.route('/crawling')
def saramin_crawling():
    page = 1
    url = 'http://highschool.saramin.co.kr/zf_user/special-recruit/list/bcode/39/code/C9/listKind/recruit/page/' \
          '%d?searchWord=' % page

    browser.get(url)
    soup = BeautifulSoup(browser.page_source)

    jobboard = soup.find('table', {'class': 'jobboard'}).findChild('tbody').findChildren('tr', 'item-row')

    for job in jobboard:
        job_a_tag = job.findChild('a', 'title')

        url = 'http://highschool.saramin.co.kr' + job_a_tag.get('href')
        title = job_a_tag.text

        company = job.findChild('div', 'company-name').first().text
        date = job.findChild('td', 'closing-date').text

        add_job_data_db(title, company, url, date)

    return redirect(url_for('job.job_list'))

    # return '<br>'.join(["%s until %s at %s" % (
    #    job.findChild('a', 'title').text, job.findChild('td', 'closing-date').text,
    #    job.findChild('div', 'company-name').first().text) for job in jobboard])
