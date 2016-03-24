# -*- coding: utf-8 -*-

"""
페이스북 Page 포스팅 하는 법 BY KCRONG
1. 유저에게 manage_pages 와 publish_pages 권한을 요청
2. https://graph.facebook.com/{page_id}?fields=access_token 으로 '페이지'의 access_token 을 가져옴
3. 가져온 페이지 access_token 으로,
    https://graph.facebook.com/{page_id}/feed 에 POST 요청을 보냄.
    (내용 요청명은 message)

    POST https://graph.facebook.com/{page_id}/feed
    message = Hello World!

!! 유저의 Access_token 으로 feed 에 요청을 보내면 유저가 페이지에 게시물을 올림.. (소용없)

"""
import json

from db_config import FACEBOOK_ALARM_USER_ACCESSTOKEN, FACEBOOK_PAGE_ID
import requests


def get_page_access_token(user_access_token):
    url = 'https://graph.facebook.com/%s?fields=access_token&access_token=%s' % (
        FACEBOOK_PAGE_ID, user_access_token)

    try:
        data = requests.get(url).json()
    except (AttributeError, TypeError):
        data = requests.get(url).json()

    return data['access_token']


def write_new_post(message):
    page_access_token = get_page_access_token(FACEBOOK_ALARM_USER_ACCESSTOKEN)

    url = 'https://graph.facebook.com/%s/feed' % FACEBOOK_PAGE_ID
    r = requests.post(url, data={
        'access_token': page_access_token,
        'message': message
    })

    print(r.text)
    try:
        return json.loads(r.text)['id']
    except KeyError:
        # 이전 게시물과 동일한 내용의 게시물을 업로드한 경우
        # TODO: EDIT
        pass

if __name__ == '__main__':
    write_new_post("새로운 취직정보!<br>sd\nsdf")
