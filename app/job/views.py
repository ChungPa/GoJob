#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import render_template

from . import job_blueprint


@job_blueprint.route('/')
def job_list():
    return render_template('job/worklist.html')
