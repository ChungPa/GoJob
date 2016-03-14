#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import render_template

from . import job_blueprint
from ..models import Job


@job_blueprint.route('/')
def job_list():
    all_job = Job.query.all()
    return render_template('job/worklist.html',
                           all_job=all_job)
