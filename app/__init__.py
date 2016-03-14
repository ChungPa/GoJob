#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import logging

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import MigrateCommand, Migrate
from flask.ext.script import Manager

app = Flask(__name__)
db = SQLAlchemy(app)

# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)


def setting_app():
    sys.path.append(app.root_path)

    from account import user_blueprint
    from job import job_blueprint
    from main import main_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(job_blueprint, url_prefix='/job')
    app.register_blueprint(user_blueprint, url_prefix='/user')

    app.config.from_pyfile('../config.py')
    return app


import models
from models import *

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
