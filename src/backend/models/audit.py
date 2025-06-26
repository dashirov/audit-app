from . import db
from datetime import datetime
import uuid

class Organization(db.Model):
    __tablename__ = 'organizations'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    audits = db.relationship('Audit', backref='organization', lazy=True)

class Audit(db.Model):
    __tablename__ = 'audits'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    org_id = db.Column(db.String, db.ForeignKey('organizations.id'), nullable=False)
    status = db.Column(db.String, default='draft')  # draft, certified
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    responses = db.relationship('AuditResponse', backref='audit', lazy=True)
    revisions = db.relationship('AuditRevision', backref='audit', lazy=True)

class AuditResponse(db.Model):
    __tablename__ = 'audit_responses'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    audit_id = db.Column(db.String, db.ForeignKey('audits.id'), nullable=False)
    category = db.Column(db.String, nullable=False)
    score = db.Column(db.Integer)
    observation_text = db.Column(db.Text)
    target_score = db.Column(db.Integer)
    improvement_text = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AuditRevision(db.Model):
    __tablename__ = 'audit_revisions'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    audit_id = db.Column(db.String, db.ForeignKey('audits.id'), nullable=False)
    snapshot_json = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.String)