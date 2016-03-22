# -*- coding: utf-8 -*-
"""
Worknet
http://www.work.go.kr
"""
from datetime import datetime
import requests

from bs4 import BeautifulSoup
from fb_manager import write_new_post
from app.models import *


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

    soup = BeautifulSoup(r.text, "html.parser")
    all_cnt = soup.find('span', {'class': 'matching'}).findChild('strong').text.replace(',', '')

    return int(all_cnt)


def get_more_info_job(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    job_condition = soup.find('li', {'class': 'condition'})
    job_form = soup.find('li', {'class': 'form'})

    address_pay = job_condition.findChildren('dd')

    address = " ".join(address_pay[0].attrMap['title'].split())
    pay = address_pay[1].text.split()[1]

    work_type = job_form.findChild('dd').text

    role = soup.find('tbody', {'class': 'form05'}).first().findChild('td').first().previousSibling.strip()

    return pay, work_type, role, address


class Worknet:
    def __init__(self):
        # all_cnt = get_all_job_cnt()
        # print "Worknet : %s" % all_cnt

        # new_job_cnt = all_cnt - Job.query.filter(Job.url.contains('www.work.go.kr')).count()
        # print "New Worknet Job: %d" % new_job_cnt
        self.new_job_cnt = 7775
        self.domain = 'http://www.work.go.kr'
        self.request_data = {
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
            'resultCnt': str(self.new_job_cnt)
        }
        self.needed_data = {
            'company': '',
            'detail_info_url': '',
            'created_date': '',
            'end_date': '',
            'location': '',

            'pay': '',
            'work_type': '',
            'role': ''
        }

    def make_soup(self, method, url, data=None):
        method = method.lower()
        import os
        html_fn = '{}.html'.format(hash(url + str(data)))
        if html_fn in os.listdir('.'):
            fp = open(html_fn, 'r')
            html = fp.read()
            fp.close()
        else:
            if method == 'get':
                res = requests.get(url, data=data)
            elif method == 'post':
                res = requests.post(url, data=data)
            else:
                print("Unsupported method")
                return False

            html = res.text

            with open(html_fn, 'w') as fp:
                fp.write(html.encode('utf-8'))

        return BeautifulSoup(html, "html.parser")

    def ss2str(self, stripped_strings):
        return list(stripped_strings)[0]

    def error_handler(self, soup, msg):
        """
        :param soup: 파일 저장위한 soup 객체
        :param msg: 에러 메세지
        """

        def error_msg(msg):
            class bcolors:
                HEADER = '\033[95m'
                OKBLUE = '\033[94m'
                OKGREEN = '\033[92m'
                WARNING = '\033[93m'
                FAIL = '\033[91m'
                ENDC = '\033[0m'
                BOLD = '\033[1m'
                UNDERLINE = '\033[4m'

            print(bcolors.FAIL + msg + bcolors.ENDC)

        error_msg(msg)
        title = soup.find('title').string
        print(title)
        try:
            fn = '{}.html'.format(title)
        except UnicodeEncodeError:
            fn = 'unicode error.html'
        with open(fn, 'wb') as fp:
            fp.write(str(soup))
        error_msg("ERROR!! Check {}".format(fn))
        import sys
        sys.exit(1)

    def get_list(self):
        """
        :return: recruit_url_list
        """
        recruit_url_list = []
        url = '{}/empInfo/empInfoSrch/list/dtlEmpSrchList.do'.format(self.domain)
        soup = self.make_soup('get', url, data=self.request_data)
        all_jobs = soup.find('tbody', {'class': 'form03'})

        for job_tr in all_jobs.findAll('tr'):
            column = job_tr.find_all('td')
            """
            column 순서:
            | 0: 체크박스 | 1: 회사명/기업형태 | 2: 채용제목/임금/근무지역 | 3: 학력/경력 | 4: 등록일 | 5: 마감일 | 6: 제공처 |
            """
            col_list = list(column)
            # company = col_list[1].string  # 회사명
            # title = col_list[2].find('p', {'class': 'link'})['title']
            detail_info_url = '{}{}'.format(self.domain, column[2].find('a')['href'])  # 상세정보 url
            recruit_url_list.append(detail_info_url)

        return recruit_url_list

    def detail_info(self, url):
        soup = self.make_soup('get', url)
        title = self.ss2str(soup.find('h3').stripped_strings)  # 채용 공고 타이틀
        tables = soup.find_all('table')
        """
            http://www.work.go.kr/empInfo/empInfoSrch/detail/empDetailAuthView.do?callPage=detail&wantedAuthNo=KJLJ001603220038&rtnUrl=/empInfo/empInfoSrch/list/dtlEmpSrchList.do?len=0&tot=0&relYn=N&totalEmpCount=0&jobsCount=0&lastIndex=1&siteClcd=all&firstIndex=1&pageSize=10&recordCountPerPage=10&preferentialGbn=all&rowNo=0&softMatchingPossibleYn=Y&benefitSrchAndOr=O&charSet=EUC-KR&startPos=0&collectionName=tb_workinfo&softMatchingMinRate=+66&softMatchingMaxRate=100&academicGbn=01|02|03&certifiYn=N&preferentialYn=Y&preferential=all&termSearchGbn=all&&empTpGbcd=1&onlyTitleSrchYn=N&onlyContentSrchYn=N&serialversionuid=3990642507954558837&resultCnt=10&sortOrderBy=DESC&sortField=DATE&pageIndex=1&pageUnit=10
            경우 테이블이 11개가 있는데
            0번째는 뭐하는건지 모르겠고

            1. 회사명 기업정보: 이 표는 회사명의 기업정보를 제공합니다.
            2. 모집요강: 자료로 모집직종, 관련직종, 직무내용, 접수마감일, 고용형태, 모집인원, 임금조건, 경력조건, 학력, 키워드에 대한 정보를 제공합니다.
            3. 우대사항: 외국어능력, 전공, 자격면허, 병역특례채용희망, 컴퓨터활용능력, 우대조건, 기타우대사항에 대한 정보를 제공합니다.
            4. 전형방법: 전형방법, 접수방법, 제출서류양식, 체출서류 준비물, 기타안내에 대한 정보를 제공합니다.
            5. null: VM1478:2 undefined
            6. 근무환경 및 복리후생: 근무예정지, 소속산업단지, 인근전철역, 근무시간/형태, 복리후생, 퇴직금, 기타복리후생, 장애인 편의시설에 대한 정보를 제공합니다.
            7. 기타입력사항: 기타입력사항에 대한 정보를 제공합니다.
            8. 채용담당자: 채용담당자에 대한 정보를 제공합니다.
            9. 회사주소: 회사주소에 대한 정보를 제공합니다.
            10. 진행중인 다른 채용공고: 회사명, 채용제목, 모집인원, 고용형태,모집마감일, 채용정보결과, 정보보기에 대한 정보를 제공합니다.
        """
        summary_element = soup.find('div', {'id': 'intereView'})  # 오타?..

        divs = list(summary_element.find_all('div'))
        # divs[0].find_all('li'): # 지원 자격, 근무 조건, 고용 형태 3가지 li return 예정
        condition = divs[0].find('li', {'class': 'condition'})  # 근무 조건

        for dt in condition.find_all('dt'):
            if dt.string == u'근무지역':
                location = self.ss2str(dt.find_next_sibling().stripped_strings)  # 회사위치인지 근무지인지.. 물론 지금은 당연히 근무지겠지만
            elif dt.string == u'임금':
                pay = self.ss2str(dt.find_next_sibling().stripped_strings)
            else:
                continue
        try:
            self.needed_data['location'] = location
            self.needed_data['pay'] = pay  # 정규식으로 숫자만
        except NameError:
            self.error_handler(soup, 'Summary nono.. omg')

        form = divs[0].find('li', {'class': 'form'})  # 고용 형태
        for dt in form.find_all('dt'):
            if dt.string == u'고용형태':
                work_type = self.ss2str(dt.find_next_sibling().stripped_strings)  # 계약직 or 정규직, employ_type
            elif dt.string == u'근무형태':
                role = self.ss2str(dt.find_next_sibling().stripped_strings)  # 주 n 일 근무, workday
            else:
                continue
        try:
            self.needed_data['work_type'] = work_type
            self.needed_data['role'] = role
        except NameError:
            self.error_handler(soup, 'employ_type and workday nono...')

        self.needed_data['title'] = title
        due_date = self.ss2str(soup.find('span', {'class': 'due'}).parent.stripped_strings)
        self.needed_data['end_date'] = datetime.strptime(due_date, u'%Y년 %m월 %d일'.encode('utf-8'))
        # 제발 python3 합시다
        self.needed_data['detail_info_url'] = url
        self.needed_data['company'] = self.ss2str(tables[1].find('td').find('strong').stripped_strings)

    def save(self):
        def get_or_create(session, model, **kwargs):
            instance = session.query(model).filter_by(**kwargs).first()
            if instance:
                return instance
            else:
                instance = model(**kwargs)
                session.add(instance)
                session.commit()
                return instance

        # title, pay, work_type, role, end_date, url, company, location, work_type,detail_info_url = ('',) * _len

        title = self.needed_data['title']
        pay = self.needed_data['pay']
        role = self.needed_data['role']
        company = self.needed_data['company']
        work_type = self.needed_data['work_type']
        end_date = self.needed_data['end_date']
        detail_info_url = self.needed_data['detail_info_url']
        location = self.needed_data['location']
        company = get_or_create(db.session, Company, name=company)

        job = Job(title, pay, work_type, role, end_date, detail_info_url)
        company.job.append(job)

        db.session.add(job)
        db.session.commit()

        content = u"""%s\n%s\n회사명: %s\n위치: %s\n급여: %s\n근무형태: %s\n마감일자: %s\n신청링크: %s""" % (
            role, title, company, location, pay, work_type, end_date, detail_info_url)

        fb_id = write_new_post(content)  # TODO: http://docs.sqlalchemy.org/en/latest/orm/events.html 이렇게 리팩토링
        job.fb_article_id = fb_id
        db.session.commit()

    def run(self):
        recruit_url_list = self.get_list()
        for url in recruit_url_list:
            self.detail_info(url)
            self.save()


if __name__ == '__main__':
    w = Worknet()
    w.run()
