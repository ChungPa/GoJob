#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import render_template, request, url_for, session, redirect

from . import user_blueprint
from ..models import User
from ..fb_manager import facebook

from ..fb_manager import get_user_school, check_sunrin


@user_blueprint.route('/')
def login_template():
    return render_template('account/login.html')


@user_blueprint.route('/fb_login')
def facebook_login():
    return facebook.authorize(callback=url_for('user.facebook_authorized',
                                               next=request.args.get('next') or request.referrer or None,
                                               _external=True))


@user_blueprint.route('/fb_login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')

    me = facebook.get('/me')

    access_token = resp['access_token']
    fb_id = me.data['id']

    if User.query.filter_by(fb_id=fb_id, active=True).first() is not None:
        # 이미 인증된 페이스북 계정입니다.
        print "DUP!!"

    # TODO: fb_id 를 유저 디비에 추가

    user_school = get_user_school(access_token)

    if check_sunrin(user_school) is False:
        print "You are not Sunrin Student!"
        return redirect(url_for('user.login_template'))

    # TODO: redirect to main
    return "need redirecting"
