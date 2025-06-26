from . import db
import uuid
import datetime


class Area(db.Model):
    __tablename__ = 'areas'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))
    subjects = db.relationship('Subject', backref='area', lazy=True)

class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    area_id = db.Column(db.String, db.ForeignKey('areas.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    objective = db.Column(db.Text, nullable=True)
    activities = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))
    rubrics = db.relationship('MaturityRubric', backref='subject', lazy=True)

class MaturityRubric(db.Model):
    __tablename__ = 'maturity_rubric'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    subject_id = db.Column(db.String, db.ForeignKey('subjects.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    level_name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))

