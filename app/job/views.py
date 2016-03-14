#!/usr/bin/env python
# -*- coding:utf-8 -*-

from datetime import date

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

    # end_date = time.strptime(end[:5], "%m/%d")
    # end_date.tm_year = date.today().year

    # strptime 을 이용해 time struct 를 생성해도 되지만, 여기서는 format 이 일정하므로 (사람인 기준) string slice 도 가능할 듯)
    # 하단 소스가 상당히 더럽다. 수정바람 TODO: EDIT HERE

    today = date.today()

    try:
        end_date = date(today.year, int(end[:2]), int(end[3:5]))
    except UnicodeEncodeError:
        # 마감이 하루 남은 경우, 사이트에 날짜가 아닌 '내일마감' 이라고 뜸. 별도 처리가 필요함.
        end_date = date(today.year, today.month, today.day+1)

    j = Job(title, url, end_date, role)
    c.job.append(j)

    db.session.add(j)


@job_blueprint.route('/crawling_saramin')
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

    # Add DB at Final
    db.session.commit()

    return redirect(url_for('job.job_list'))

    # return '<br>'.join(["%s until %s at %s" % (
    #    job.findChild('a', 'title').text, job.findChild('td', 'closing-date').text,
    #    job.findChild('div', 'company-name').first().text) for job in jobboard])
