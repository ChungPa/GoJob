# -*- coding: utf-8 -*-
"""
Worknet
http://www.work.go.kr
"""
import time
import requests

from BeautifulSoup import BeautifulSoup
from db_manager import add_job_data_db
from fb_manager import write_new_post
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from app.models import db


def get_all_job_cnt():
    r = requests.post('http://www.work.go.kr/empInfo/empInfoSrch/list/dtlEmpSrchList.do',
                      data={
                          'moreCon': "",
                          'tabMode': "",
                          'siteClcd': "all",
                          'keyword': "",
                          'region': "",
                          'regionNm': "",
                          'occupation': "",
                          'occupationNm': "",
                          'payGbn': "noPay",
                          'minPay': "",
                          'maxPay': "",
                          'academicGbn': "00,01,02,03",
                          'careerTypes': "N",
                          'preferentialGbn': "all",
                          'resultCnt': "1"
                      })
    soup = BeautifulSoup(r.text)
    all_cnt = soup.find('span', {'class': 'matching'}).findChild('strong').text.replace(',', '')

    return int(all_cnt)


def get_more_info_job(url):
    r = requests.get(url)

    soup = BeautifulSoup(r.text)

    job_condition = soup.find('li', {'class': 'condition'})
    job_form = soup.find('li', {'class': 'form'})

    address_pay = job_condition.findChildren('dd')

    address = " ".join(address_pay[0]._getAttrMap()['title'].split())
    pay = address_pay[1].text.split()[1]

    work_type = job_form.findChild('dd').text

    role = soup.find('tbody', {'class': 'form05'}).first().findChild('td').first().previousSibling.strip()

    return pay, work_type, role, address


def get_all_job():
    all_cnt = get_all_job_cnt()
    print "Worknet : %s" % all_cnt
    r = requests.post('http://www.work.go.kr/empInfo/empInfoSrch/list/dtlEmpSrchList.do',
                      data={
                          'moreCon': "",
                          'tabMode': "",
                          'siteClcd': "all",
                          'keyword': "",
                          'region': "",
                          'regionNm': "",
                          'occupation': "",
                          'occupationNm': "",
                          'payGbn': "noPay",
                          'minPay': "",
                          'maxPay': "",
                          'academicGbn': "00,01,02,03",
                          'careerTypes': "N",
                          'preferentialGbn': "all",
                          'x': "30",
                          'y': "18",
                          'resultCnt': str(all_cnt)
                      })
    soup = BeautifulSoup(r.text)
    all_jobs = soup.find('tbody', {'class': 'form03'}).findChildren('tr')

    for job in all_jobs:
        # 제목, 급여, 업무형태, 업무역할, 마감일자, 주소, url
        # 제목,                         마감일자  주소, url
        company_td, title_td = job.findChildren('td', {'class': 'title'})
        company = company_td.findChild('a').text
        title_root = title_td.findChild('p', {'class': 'link'})
        title = title_root._getAttrMap()['title']
        url = 'http://www.work.go.kr' + title_root.findChild('a')._getAttrMap()['href']

        end_date_string = job.findChildren('td')[5].text

        try:
            end_date_struct = time.strptime(end_date_string, '%y-%m-%d')
        except ValueError:
            # 홈페이지에 "채용시까지 (16-01-01)" 라고 되어있는 공고가 있음. 따라서 괄호 안 날짜만 파싱
            end_date_struct = time.strptime(end_date_string[end_date_string.find('(') + 1:-1], '%y-%m-%d')
        finally:
            end_date = datetime.fromtimestamp(time.mktime(end_date_struct))

        pay, work_type, role, location = get_more_info_job(url)

        try:
            job_db = add_job_data_db(title, company, url, end_date, location, pay, work_type, role)
        except IntegrityError:
            db.session.rollback()
            continue
        else:
            content = u"""%s\n%s\n회사명: %s\n위치: %s\n급여: %s\n근무형태: %s\n마감일자: %s\n신청링크: %s""" % (
                role, title, company, location, pay, work_type, end_date, url)

            fb_id = write_new_post(content)

            job_db.fb_article_id = fb_id

            db.session.commit()
            print "Uploaded"

    print "Worknet Crawling Done."


if __name__ == '__main__':
    get_all_job()
