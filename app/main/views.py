#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import os.path
from urllib2 import urlopen

from flask import render_template, send_from_directory, redirect, url_for

from . import main_blueprint


def get_commit_cnt():

    user_data = json.loads(urlopen('https://api.github.com/repos/ChungPa/GoJob/contributors').read())
    contributors = dict((user['login'], user['contributions']) for user in user_data)

    return contributors


@main_blueprint.route('/')
@main_blueprint.route('/intro')
def index():
    return render_template('main/index.html')


@main_blueprint.route('/works')
def works():
    return redirect(url_for('job.job_list'))


@main_blueprint.route('/aboutus')
def about():
    contributors = get_commit_cnt()
    return render_template('main/about.html',
                           contributors=contributors)


# For Static

@main_blueprint.route('/img/<path:filename>')
def static_img(filename):
    return send_from_directory(os.path.join(main_blueprint.static_folder, 'img'), filename)


@main_blueprint.route('/font/<path:filename>')
def static_font(filename):
    return send_from_directory(os.path.join(main_blueprint.static_folder, 'font'), filename)


@main_blueprint.route('/fonts/<path:filename>')
def static_fonts(filename):
    return send_from_directory(os.path.join(main_blueprint.static_folder, 'fonts'), filename)


@main_blueprint.route('/min/<path:filename>')
def static_min(filename):
    return send_from_directory(os.path.join(main_blueprint.static_folder, 'min'), filename)


@main_blueprint.route('/css/<path:filename>')
def static_css(filename):
    return send_from_directory(os.path.join(main_blueprint.static_folder, 'css'), filename)
