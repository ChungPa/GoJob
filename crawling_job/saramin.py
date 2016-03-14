# -*-coding: utf-8 -*-
from app.models import *

from datetime import date
from selenium import webdriver
from BeautifulSoup import BeautifulSoup
from sqlalchemy.exc import IntegrityError

browser = webdriver.PhantomJS()


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
    # 하단 소스가 상당히 더럽다. 수정바람

    today = date.today()

    try:
        end_date = date(today.year, int(end[:2]), int(end[3:5]))
    except UnicodeEncodeError:
        # 마감이 하루 남은 경우, 사이트에 날짜가 아닌 '내일마감' 이라고 뜸. 별도 처리가 필요함.
        end_date = date(today.year, today.month, today.day + 1)

    j = Job(title, url, end_date, role)
    c.job.append(j)

    db.session.add(j)


def saramin_crawling():
    """
    http://highschool.saramin.co.kr/zf_user/highschool/jobs/major-list?pageCount=0
    Get Job_info Count from here.
    """
    page = 1
    url = 'http://highschool.saramin.co.kr/zf_user/highschool/jobs/major-list?category=major006&page=%d' % page

    browser.get(url)
    soup = BeautifulSoup(browser.page_source)

    all_board = soup.find('table', {'id': 'jobboard_basic'}).findChild('tbody').findChildren('tr')

    all_job = [board for board in all_board if board.get('class') != 'position-detail']

    for job in all_job:
        job_a_tag = job.findChild('a', {'class': 'link_title_recruit'})

        url = 'http://highschool.saramin.co.kr' + job_a_tag.get('href')
        title = job_a_tag.get('title')

        company = job.findChild('div', 'corp_name').first().text
        date = job.findChildren('td')[4].text

        add_job_data_db(title, company, url, date)

    # Add DB at Final
    db.session.commit()

    return True


if __name__ == '__main__':
    saramin_crawling()
    print "Done."
