from flask import Blueprint, request, jsonify
from models.audit import db, Organization, Audit, AuditResponse, AuditRevision

audit_bp = Blueprint('audit_bp', __name__)

@audit_bp.route('/orgs', methods=['POST'])
def create_org():
    data = request.json
    org = Organization(name=data['name'])
    db.session.add(org)
    db.session.commit()
    return jsonify({"id": org.id, "name": org.name})

@audit_bp.route('/orgs/<org_id>/audits', methods=['POST'])
def create_audit(org_id):
    audit = Audit(org_id=org_id)
    db.session.add(audit)
    db.session.commit()
    return jsonify({"id": audit.id, "status": audit.status})

@audit_bp.route('/audits/<audit_id>/responses', methods=['POST'])
def save_response(audit_id):
    data = request.json
    response = AuditResponse(
        audit_id=audit_id,
        category=data['category'],
        score=data.get('score'),
        observation_text=data.get('observation_text'),
        target_score=data.get('target_score'),
        improvement_text=data.get('improvement_text')
    )
    db.session.merge(response)
    db.session.commit()
    return jsonify({"status": "saved"})

@audit_bp.route('/audits/<audit_id>/revisions', methods=['POST'])
def save_revision(audit_id):
    data = request.json
    revision = AuditRevision(
        audit_id=audit_id,
        snapshot_json=data['snapshot_json'],
        author=data.get('author')
    )
    db.session.add(revision)
    db.session.commit()
    return jsonify({"status": "revision saved"})

if __name__ == '__main__':
    app.run(debug=True)
