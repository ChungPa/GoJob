#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import render_template

from . import main_blueprint


@main_blueprint.route('/')
def index():
    return render_template('main/index.html')