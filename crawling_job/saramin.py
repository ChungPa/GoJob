# -*-coding: utf-8 -*-
from app.models import *

from datetime import date
from selenium import webdriver
from BeautifulSoup import BeautifulSoup
from sqlalchemy.exc import IntegrityError

browser = webdriver.PhantomJS()


def get_cnt_major(major):
    """
    :param major:
     major001: 전기/전자/기계
     major002: 정보처리/E-비즈/콘텐츠
     major003: 호텔/조리/관광/미용
     major004: 건축/토목/인테리어
     major005: 제품/산업/시각디자인
     major006: 금융/회계/재무
     major007: 경영/비즈니스/비서
     major008: 유통/물류/국제통상
     major009: 방송/영상/멀티미디어
     major010: 보건/간호

    :return:
        해당 major (전기,호텔..etc) 의 총 채용정보 갯수 (int)
    """

    url = 'http://highschool.saramin.co.kr/zf_user/highschool/jobs/major-list?pageCount=0&category=%s' % major

    browser.get(url)
    soup = BeautifulSoup(browser.page_source)

    return soup.find('div', {'class': 'panel_bottom'}).findChild('div', {'class': 'text01'}).first().text


def add_job_data_db(title, company, url, end_date, location, pay, work_style, role):
    c = Company(company)

    db.session.add(c)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        c = Company.query.filter_by(name=company).first()

    j = Job(title, pay, location, work_style, role, end_date, url)
    c.job.append(j)

    db.session.add(j)

    db.session.commit()


def get_job_info(url):
    browser.get(url)
    soup = BeautifulSoup(browser.page_source)

    a = soup.find('table', {'class': 'rct_view_info'}).findChild('tbody').findChildren('tr')

    # 지역
    location = soup.find('div', {'class': 'recruit_summary'}).findChild('tbody').findChildren('tr')[0].findChild(
        'td').find('span').first().previousSibling.strip()

    # 급여
    pay = soup.find('div', {'class': 'recruit_summary'}).findChild('tbody').findChildren('tr')[1].findChild('td').text

    # 근무형태
    work_style = soup.find('div', {'class': 'recruit_summary'}).findChild('tbody').findChildren('tr')[2].findChild(
        'td').text

    """
        # 근무요일
        work_day = soup.find('div', {'class': 'recruit_summary'}).findChild('tbody').findChildren('tr')[3].findChild(
            'td').text
    """
    return location, pay, work_style


def saramin_crawling():
    major_list = ['major00' + str(_) for _ in xrange(1, 10)]

    for major in major_list:
        major_cnt = get_cnt_major(major)
        url = 'http://highschool.saramin.co.kr/zf_user/highschool/jobs/major-list?' \
              'category=%s&pageCount=%s' % (major, major_cnt)

        browser.get(url)
        soup = BeautifulSoup(browser.page_source)

        all_board = soup.find('table', {'id': 'jobboard_basic'}).findChild('tbody').findChildren('tr')

        all_job = [board for board in all_board if board.get('class') != 'position-detail']

        for job in all_job:
            job_a_tag = job.findChild('a', {'class': 'link_title_recruit'})

            url = 'http://highschool.saramin.co.kr' + job_a_tag.get('href')

            location, pay, work_style = get_job_info(url)

            title = job_a_tag.get('title')

            company = job.findChild('div', 'corp_name').first().text
            end_date = job.findChildren('td')[4].text

            # end_date = time.strptime(end[:5], "%m/%d")
            # end_date.tm_year = date.today().year

            # strptime 을 이용해 time struct 를 생성해도 되지만, 여기서는 format 이 일정하므로 (사람인 기준) string slice 도 가능할 듯)
            # 하단 소스가 상당히 더럽다. 수정바람

            today = date.today()

            try:
                end_date = date(today.year, int(end_date[:2]), int(end_date[3:5]))
            except UnicodeEncodeError:
                # 마감이 하루 남은 경우, 사이트에 날짜가 아닌 '내일마감' 이라고 뜸. 별도 처리가 필요함.
                end_date = date(today.year, today.month, today.day + 1)

            # def add_job_data_db(title, company, url, end_date, location, pay, work_style, role)
            add_job_data_db(title, company, url, end_date, location, pay, work_style, major)

    return True


if __name__ == '__main__':
    saramin_crawling()
    print "Done."
