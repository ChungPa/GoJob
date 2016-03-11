#!/usr/bin/env python
# -*- coding:utf-8 -*-
from BeautifulSoup import BeautifulSoup
from flask import render_template
from selenium import webdriver

from . import job_blueprint

browser = webdriver.PhantomJS()


@job_blueprint.route('/')
def job_list():
    return render_template('job/worklist.html')


@job_blueprint.route('/crawling')
def saramin_crawling():
    page = 1
    url = 'http://highschool.saramin.co.kr/zf_user/special-recruit/list/bcode/39/code/C9/listKind/recruit/page/' \
          '%d?searchWord=' % page

    browser.get(url)
    soup = BeautifulSoup(browser.page_source)

    jobboard = soup.find('table', {'class': 'jobboard'}).findChild('tbody').findChildren('tr', 'item-row')

    """
        for job in jobboard:
            job_a_tag = job.findChild('a', 'title')

            url = job_a_tag.get('href')
            title = job_a_tag.text

            company = job.findChild('div', 'company-name').first().text
            date = job.findChild('td', 'closing-date').text

            print "%s hire until %s" % (company, date)
    """

    return '<br>'.join(["%s until %s at %s" % (job.findChild('a', 'title').text, job.findChild('td', 'closing-date').text, job.findChild('div', 'company-name').first().text) for job in jobboard])


