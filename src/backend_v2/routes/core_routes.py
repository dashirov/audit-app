
from flask import Blueprint, request, jsonify
from models import db
from models.core import Organization, OrganizationalRole, Practice, PracticeAspect, AspectCapability, MaturityRubric, \
    ReflectivePrompt, QualitativePrompt, AuditEffort, AssessmentResponse, OrganizationMember
from datetime import datetime, timezone
import uuid

core_bp = Blueprint('core_bp', __name__)


def generate_uuid():
    return str(uuid.uuid4())

@core_bp.route('/audits/<audit_id>', methods=['GET'])
def get_audit_by_id(audit_id):
    """
    Retrieve a single audit effort by ID.
    Response JSON: {
        "id": UUID,
        "name": string,
        "organization_id": UUID,
        "created_at": timestamp,
        "updated_at": timestamp,
        ...
    }
    """
    audit = AuditEffort.query.get(audit_id)
    if audit is None:
        return jsonify({'error': 'Audit not found'}), 404
    # If the model has a to_dict, use it; otherwise, manually serialize
    if hasattr(audit, 'to_dict'):
        return jsonify(audit.to_dict())
    else:
        return jsonify({
            "id": audit.id,
            "name": audit.name,
            "organization_id": audit.organization_id,
            "created_at": audit.created_at,
            "updated_at": audit.updated_at,
            "auditor": getattr(audit, "auditor", None),
            "status": getattr(audit, "status", None),
        })

@core_bp.route('/organizations', methods=['POST'])
def create_organization():
    """
    Create a new organization.
    Request JSON: { "name": "Organization Name" }
    Response JSON: { "id": UUID, "name": "Organization Name" }
    """
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Name is required'}), 400

    organization = Organization(name=name)
    db.session.add(organization)
    db.session.commit()
    return jsonify({'id': organization.id, 'name': organization.name}), 200

@core_bp.route('/organizations/<org_id>/audit', methods=['POST'])
def create_audit(org_id):
    """
    Create a new audit for an organization.
    Request JSON: {"name": str, "auditor": str (optional) }
    Response JSON: { "id": UUID, "org_id": UUID, "name": str, "status": str }
    """
    data = request.get_json()
    name = data.get('name')
    auditor = data.get('auditor')

    if not org_id or not name:
        return jsonify({'error': 'org_id and name are required'}), 400

    conflict = AuditEffort.query.filter_by(organization_id=org_id, name=data["name"]).first()
    if conflict:
        return jsonify({"error": "Audit effort with this name already exists"}), 400

    audit = AuditEffort(
        organization_id=org_id,
        name=name,
        auditor=auditor,
        status='draft'
    )

    db.session.add(audit)
    db.session.commit()
    return jsonify({
        'id': audit.id,
        'organization_id': audit.organization_id,
        'name': audit.name,
        'status': audit.status
    }), 200

@core_bp.route('/organizations/<org_id>/audits', methods=['GET'])
def get_organization_audits(org_id):
    """
    Retrieve the organization by UUID.
    Response JSON: { "id": UUID, "name": "Organization Name" }
    """
    efforts = AuditEffort.query.filter_by(organization_id=org_id)
    return jsonify([{'id': e.id, 'name': e.name, 'status': e.status, 'organization_id': e.organization_id} for e in efforts]), 200



@core_bp.route('/organizations/<org_id>', methods=['GET'])
def get_organization_by_id(org_id):
    """
    Retrieve the organization by UUID.
    Response JSON: { "id": UUID, "name": "Organization Name" }
    """
    org = Organization.query.get(org_id)
    if not org:
        return jsonify({'error': 'Organization not found'}), 404
    return jsonify({'id': org.id, 'name': org.name, 'created_at': org.created_at, 'updated_at': org.updated_at})


@core_bp.route('/organizations/by-name/<name>', methods=['GET'])
def get_organization_by_name(name):
    """
    Retrieve organization by its name.
    Response JSON: { "id": UUID, "name": "Organization Name" }
    """
    org = Organization.query.filter_by(name=name).first()
    if not org:
        return jsonify({'error': 'Organization not found'}), 404
    return jsonify({'id': org.id, 'name': org.name})


@core_bp.route('/organizations', methods=['GET'])
def list_organizations():
    """
    List all organizations.
    Response JSON: [ { "id": UUID, "name": "Organization Name" }, ... ]
    """
    orgs = Organization.query.all()
    return jsonify([{'id': o.id, 'name': o.name} for o in orgs])


@core_bp.route('/organizational_roles', methods=['GET'])
def get_roles():
    """
    List all organizational roles.
    Response JSON: [ { "id": UUID, "name": "Role Name" }, ... ]
    """
    roles = OrganizationalRole.query.all()
    return jsonify([{'id': role.id, 'name': role.name} for role in roles])


@core_bp.route("/organizations/<org_id>/members", methods=["POST"])
def create_organization_member(org_id):
    """
    Create a new organization member and assign roles.

    Payload:
    {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "slack_handle": "@jane",
        "teams_handle": "jane_doe_teams",
        "role_ids": ["role-uuid-1", "role-uuid-2"]
    }
    """
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    slack_handle = data.get("slack_handle")
    teams_handle = data.get("teams_handle")
    role_ids = data.get("role_ids", [])

    if not name or not email:
        return jsonify({"error": "name and email are required"}), 400

    member = OrganizationMember(
        name=name,
        email=email,
        slack_handle=slack_handle,
        teams_handle=teams_handle,
        organization_id=org_id
    )

    for role_id in role_ids:
        role = db.session.get(OrganizationalRole, role_id)
        if role:
            member.roles.append(role)

    db.session.add(member)
    db.session.commit()

    return jsonify({
        "message": "Member created",
        "id": member.id
    }), 200


# Retrieve all members of a given organization.
@core_bp.route("/organizations/<org_id>/members", methods=["GET"])
def get_organization_members(org_id):
    """
    Retrieve all members of a given organization.

    Response JSON:
    [
        {
            "id": UUID,
            "name": str,
            "email": str,
            "slack_handle": str or null,
            "teams_handle": str or null,
            "role_ids": [UUID, ...],
            "role_names": [str, ...]
        },
        ...
    ]
    """
    members = OrganizationMember.query.filter_by(organization_id=org_id).all()
    result = []
    for member in members:
        result.append({
            "id": member.id,
            "name": member.name,
            "email": member.email,
            "slack_handle": member.slack_handle,
            "teams_handle": member.teams_handle,
            "role_ids": [role.id for role in member.roles],
            "role_names": [role.name for role in member.roles]
        })

    return jsonify(result), 200

@core_bp.route('/practices', methods=['GET'])
def get_practices():
    """
    List all practice areas.
    Response JSON: [ { "id": UUID, "name": "Practice Name" }, ... ]
    """
    practices = Practice.query.all()
    return jsonify([{'id': p.id, 'name': p.name} for p in practices])


@core_bp.route('/practice_aspects/<practice_id>', methods=['GET'])
def get_practice_aspects(practice_id):
    """
    List practice aspects for a given practice.
    Response JSON: [ { "id": UUID, "name": "Aspect Name" }, ... ]
    """
    aspects = PracticeAspect.query.filter_by(practice_id=practice_id).all()
    return jsonify([{'id': a.id, 'name': a.name} for a in aspects])


@core_bp.route('/aspect_capabilities/<aspect_id>', methods=['GET'])
def get_aspect_capabilities(aspect_id):
    """
    List capabilities for a given practice aspect.
    Response JSON: [ { "id": UUID, "name": "Capability Name" }, ... ]
    """
    capabilities = AspectCapability.query.filter_by(practice_aspect_id=aspect_id).all()
    return jsonify([{'id': c.id, 'name': c.name} for c in capabilities])


@core_bp.route('/rubrics/<capability_id>', methods=['GET'])
def get_rubrics(capability_id):
    """
    Get the maturity rubric levels for a given capability.
    Response JSON: [ { "score": int, "level_name": str, "state": str }, ... ]
    """
    rubrics = MaturityRubric.query.filter_by(aspect_capability_id=capability_id).all()
    return jsonify([{
        'score': r.score,
        'level_name': r.level_name,
        'state': r.state
    } for r in rubrics])


@core_bp.route('/reflective_prompts/<aspect_id>', methods=['GET'])
def get_reflective_prompts(aspect_id):
    """
    Get reflective prompts for a given practice aspect.
    Response JSON: [ { "id": UUID, "prompt": str, "insight_goal": str }, ... ]
    """
    prompts = ReflectivePrompt.query.filter_by(practice_aspect_id=aspect_id).all()
    return jsonify([{
        'id': p.id,
        'prompt': p.prompt,
        'insight_goal': p.insight_goal
    } for p in prompts])


@core_bp.route('/qualitative_prompts/<capability_id>', methods=['GET'])
def get_qualitative_prompts(capability_id):
    """
    Get qualitative prompts for a given capability.
    Response JSON: [ { "id": UUID, "prompt": str }, ... ]
    """
    prompts = QualitativePrompt.query.filter_by(aspect_capability_id=capability_id).all()
    return jsonify([{
        'id': p.id,
        'prompt': p.prompt
    } for p in prompts])


@core_bp.route('/audit_efforts', methods=['POST'])
def create_audit_effort():
    """
    Create a new audit effort for a given organization.
    Request JSON: { "name": str, "organization_id": UUID, "auditor": str (optional) }
    Response JSON: { "id": UUID, "name": str }
    """
    data = request.get_json()
    name = data.get('name')
    organization_id = data.get('organization_id')
    auditor = data.get('auditor')

    if not name or not organization_id:
        return jsonify({'error': 'Name and organization_id are required'}), 400

    audit = AuditEffort(
        name=name,
        organization_id=organization_id,
        auditor=auditor,
        status='draft'
    )
    db.session.add(audit)
    db.session.commit()
    return jsonify({'id': audit.id, 'name': audit.name}), 201


@core_bp.route('/assessment_responses', methods=['POST'])
def post_assessment_response():
    """
    Submit an assessment response for a capability.
    Request JSON: {
      "audit_id": UUID,
      "practice_id": UUID,
      "practice_aspect_id": UUID,
      "aspect_capability_id": UUID,
      "role_id": UUID,
      "score": int,
      "notes": str (optional),
      "evidence": str (optional)
    }
    Response JSON: { "id": UUID, "score": int }
    """
    data = request.get_json()

    response = AssessmentResponse(
        audit_id=data['audit_id'],
        practice_id=data['practice_id'],
        practice_aspect_id=data['practice_aspect_id'],
        aspect_capability_id=data['aspect_capability_id'],
        role_id=data['role_id'],
        score=data['score'],
        notes=data.get('notes', ''),
        evidence=data.get('evidence', '')
    )
    db.session.add(response)
    db.session.commit()

    return jsonify({'id': response.id, 'score': response.score}), 201


@core_bp.route('/assessment_responses/<audit_id>', methods=['GET'])
def get_assessment_responses(audit_id):
    """
    Retrieve all assessment responses for a given audit.
    Response JSON: [ { "id": UUID, "capability_id": UUID, "role_id": UUID, "score": int, "notes": str, "evidence": str }, ... ]
    """
    responses = AssessmentResponse.query.filter_by(audit_id=audit_id).all()
    return jsonify([{
        'id': r.id,
        'capability_id': r.aspect_capability_id,
        'role_id': r.role_id,
        'score': r.score,
        'notes': r.notes,
        'evidence': r.evidence
    } for r in responses])


@core_bp.route('/undo_last_response/<audit_id>', methods=['POST'])
def undo_last_response(audit_id):
    """
    Undo the last assessment response for a given audit.
    Response JSON: { "message": str } or 404 error if no response found.
    """
    response = AssessmentResponse.query.filter_by(audit_id=audit_id).order_by(
        AssessmentResponse.created_at.desc()).first()
    if not response:
        return jsonify({'error': 'No responses found to undo.'}), 404

    db.session.delete(response)
    db.session.commit()
    return jsonify({'message': 'Last response deleted.'}), 200

@core_bp.route('/organizations/<org_id>/members/<member_id>', methods=['DELETE'])
def delete_organization_member(org_id, member_id):
    """
    Delete a member from an organization.
    """
    member = OrganizationMember.query.filter_by(id=member_id, organization_id=org_id).first()
    if not member:
        return jsonify({"error": "Member not found"}), 404

    db.session.delete(member)
    db.session.commit()
    return jsonify({"message": "Member deleted", "id": member.id}), 200


# Update an existing member of an organization and their associated roles.
@core_bp.route('/organizations/<org_id>/members/<member_id>', methods=['PUT'])
def update_organization_member(org_id, member_id):
    """
    Update an existing member of an organization and their associated roles.
    Request JSON: {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "slack_handle": "@janedoe",
        "teams_handle": "@teamsjanedoe",
        "role_ids": [UUID, UUID]
    }
    """
    data = request.get_json()
    member = OrganizationMember.query.filter_by(id=member_id, organization_id=org_id).first_or_404()

    member.name = data.get('name')
    member.email = data.get('email')
    member.slack_handle = data.get('slack_handle')
    member.teams_handle = data.get('teams_handle')

    # Clear existing roles
    member.roles.clear()

    # Reassign new roles
    if 'role_ids' in data:
        roles = OrganizationalRole.query.filter(OrganizationalRole.id.in_(data['role_ids'])).all()
        member.roles.extend(roles)

    db.session.commit()

    return jsonify({
        "id": str(member.id),
        "name": member.name,
        "email": member.email,
        "slack_handle": member.slack_handle,
        "teams_handle": member.teams_handle,
        "role_names": [role.name for role in member.roles]
    })