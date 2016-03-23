#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import render_template, request

from . import job_blueprint
from app.models import Job

from werkzeug.exceptions import BadRequest


@job_blueprint.route('/')
def job_list():
    try:
        query = request.args['query']
    except BadRequest:
        query = ""

    all_job = Job.query.filter(Job.title.contains(query) | Job.pay.contains(query) | Job.work_style.contains(query) | Job.role.contains(query) | Job.url.contains(query)).all()
    return render_template('job/worklist.html',
                           all_job=all_job)
