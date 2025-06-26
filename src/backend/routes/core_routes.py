from flask import Blueprint, request, jsonify
from models.core import Subject, MaturityRubric

core_bp = Blueprint('core_bp', __name__)

# Load subjects from database
@core_bp.route("/subject")
def get_subject():
    subjects = Subject.query.all()
    result = [
        {
            "id": s.id,
            "name": s.name,
            "objective": s.objective,
            "activities": s.activities
        }
        for s in subjects
    ]
    return jsonify(result)

# Load rubric levels from database
@core_bp.route("/rubric")
def get_rubric():
    rubrics = MaturityRubric.query.all()
    result = [
        {
            "id": r.id,
            "subject_id": r.subject_id,
            "score": r.score,
            "description": r.description,
            "category": r.subject.name,
            "level_name": r.level_name
        }
        for r in rubrics
    ]
    return jsonify(result)

@core_bp.route('/')
def home():
    return open("frontend/index.html").read()
