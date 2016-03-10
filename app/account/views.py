#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import render_template

from . import user_blueprint


@user_blueprint.route('/')
def login_tempalate():
    return render_template('account/login.html')
