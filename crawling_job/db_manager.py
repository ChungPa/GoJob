from app.models import *
from sqlalchemy.exc import IntegrityError


def add_job_data_db(title, company, url, end_date, location, pay, work_style, role):
    c = Company(company, location)

    db.session.add(c)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        c = Company.query.filter_by(name=company).first()

    j = Job(title, pay, work_style, role, end_date, url)
    c.job.append(j)

    db.session.add(j)

    db.session.commit()

    return j
