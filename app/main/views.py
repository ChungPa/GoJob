#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os.path

from flask import render_template, send_from_directory

from . import main_blueprint


@main_blueprint.route('/')
def index():
    return render_template('main/index.html')


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