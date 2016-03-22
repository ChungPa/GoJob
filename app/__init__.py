#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys

from flask import Flask
from flask.ext.migrate import MigrateCommand, Migrate
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('../config.py')
db = SQLAlchemy(app)


def setting_app():
    sys.path.append(app.root_path)

    from job import job_blueprint
    from main import main_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(job_blueprint, url_prefix='/job')

    return app


import models
from models import *

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.template_filter('totitle')
def index_rank(title):
    if len(unicode(title)) > 13:
        return title[:10] + '...'
    else:
        return title
