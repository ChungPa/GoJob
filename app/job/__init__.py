#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Blueprint

job_blueprint = Blueprint('job', __name__)

from . import views