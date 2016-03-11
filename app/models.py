#!/usr/bin/env python
# -*- coding:utf-8 -*-

from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(10), nullable=False)

    userid = db.Column(db.String(30), unique=True, nullable=False)
    userpw = db.Column(db.String(30), nullable=False)

    fb_id = db.Column(db.String(100), nullable=False, unique=True)
    fb_accesstoken = db.Column(db.String(200), nullable=False, unique=True)

    created = db.Column(db.DATETIME, default=datetime.now())
    updated = db.Column(db.DATETIME, default=datetime.now(), onupdate=datetime.now())

    active = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, name, userid, userpw, fb_id, fb_accesstoken):
        self.name = name
        self.userid = userid
        self.userpw = userpw
        self.fb_id = fb_id
        self.fb_accesstoken = fb_accesstoken

    def __repr__(self):
        return "<User %s>" % self.userid


class Company(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(70), nullable=False)
    job_id = db.Column(db.INTEGER, db.ForeignKey('job.id'))

    def __init__(self, name, location):
        self.name = name
        self.location = location

    def __repr__(self):
        return "<Company %s>" % self.name


class Job(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    money = db.Column(db.INTEGER, nullable=False)
    role = db.Column(db.String(30), nullable=False)

    company = db.relationship(Company, backref='job')

    created = db.Column(db.DATETIME, default=datetime.now(), nullable=False)
    end = db.Column(db.DATE, nullable=False)

    def __init__(self, title, company, money, location, role):
        self.title = title
        self.company = company
        self.money = money
        self.location = location
        self.role = role

    def __repr__(self):
        return "<Job %s>" % self.company
