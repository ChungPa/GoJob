# -*-coding: utf-8 -*-
import requests
from flask_oauth import OAuth
from flask import session
from config import FACEBOOK_APP_ID, FACEBOOK_APP_SECRET

oauth = OAuth()
sunrin_keyword = [u'선린', u'sunrin']


def check_sunrin(school):
    return any([keyword in school.lower() for keyword in sunrin_keyword])


def get_user_school(access_token):
    url = 'https://graph.facebook.com/me?access_token=%s&fields=education' % access_token

    json_school_data = requests.get(url).json()

    try:
        return json_school_data['education'][0]['school']['name']
    except KeyError:
        return "No School"


facebook = oauth.remote_app('facebook',
                            base_url='https://graph.facebook.com/',
                            request_token_url=None,
                            access_token_url='/oauth/access_token',
                            authorize_url='https://www.facebook.com/dialog/oauth',
                            consumer_key=FACEBOOK_APP_ID,
                            consumer_secret=FACEBOOK_APP_SECRET,
                            # Request Permission
                            # user_education_history = User's Education_history for get user's school
                            request_token_params={
                                'scope': ['user_education_history']}
                            )


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')
