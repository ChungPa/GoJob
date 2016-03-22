#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Blueprint

job_blueprint = Blueprint('myjob', __name__)

from . import views
