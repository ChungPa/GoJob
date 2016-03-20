import requests
from flask import request

from db_config import KAKAO_APP_ID, KAKAO_APP_ADMIN_KEY, GCM_PUSH_TOKEN


def get_kakao_access_token(user_code):
    r = requests.post("https://kauth.kakao.com/oauth/token",
                      data={
                          'grant_type': 'authorization_code',
                          'client_id': KAKAO_APP_ID,
                          'code': user_code,
                          'redirect_uri': request.base_url
                      })

    return r.json()['access_token']


def get_kakao_user_id(access_token):
    headers = {
        'Authorization': ('Bearer %s' % access_token),
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
    }

    r = requests.post("https://kapi.kakao.com/v1/user/me",
                      headers=headers
                      )
    return r.json()['id']


def register_kakao_push_token(userid):
    header = {
        'Authorization': ('KakaoAK %s' % KAKAO_APP_ADMIN_KEY)
    }

    r = requests.post('https://kapi.kakao.com/v1/push/register',
                      headers=header,
                      data={
                          'uuid': userid,
                          'device_id': userid,
                          'push_type': 'gcm',
                          'push_token': GCM_PUSH_TOKEN
                      })
    r.text
