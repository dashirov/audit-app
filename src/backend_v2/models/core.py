import datetime
import uuid
from models import db


def generate_uuid():
    return str(uuid.uuid4())
def generate_timestamp():
    return datetime.datetime.now(datetime.UTC)


class Organization(db.Model):
    """
    Organization – Represents a single entity (e.g., a company, nonprofit, or department) undergoing one or more audit efforts.

    Each organization is uniquely identified by a UUID. The name of the organization is also unique (alternative key).
    Organizations may undergo multiple audit efforts over time, each capturing observations, assessments, and
    improvement plans for different subject areas.

    Fields:
      - id: Unique identifier (UUID).
      - name: Human-readable name of the organization.
      - created_at / updated_at: Timestamps for lifecycle tracking.
      - audit_efforts: Relationship mapping to multiple audit efforts tied to this organization.

    Example:
      Organization(name="ACME Corp.") could have two audit efforts:
        - 2024 Data Engineering Assessment (draft)
        - 2023 Corporate Reporting Certification (certified)
    """
    __tablename__ = 'organization'

    id = db.Column(db.Uuid, primary_key=True, default=generate_uuid)
    created_at = db.Column(db.DateTime, default=generate_timestamp)
    updated_at = db.Column(db.DateTime, default=generate_timestamp)

    name = db.Column(db.String, nullable=False)

    organization_members = db.relationship('OrganizationMember', backref='organization', lazy=True)
    audit_efforts = db.relationship('AuditEffort', backref='organization', lazy=True)

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            name=data.get("name")
        )
    @classmethod
    def from_list(cls, data):
        return [cls.from_dict(x) for x in data]


class OrganizationalRole(db.Model):
    """
    OrganizationalRole – Represents a stakeholder role within the organization whose viewpoint is assessed during the audit process.

    This role is used to associate interview questions (qualitative or reflective) with specific organizational functions,
    ensuring relevant and contextual responses during the audit process.

    Examples include:
      - Data Engineer: Technical contributor with deep understanding of infrastructure and systems.
      - Product Analyst: Analyst responsible for product usage insights and behavioral metrics.
      - Member of the Board: Senior stakeholder with limited technical exposure but strategic oversight.

    Fields:
      - id: Unique identifier for the role.
      - name: Name of the role (e.g., "Product Analyst", "Executive Leader").
      - created_at / updated_at: Timestamps for lifecycle tracking.

    Usage:
      Role definitions are referenced when configuring assessments, mapping interview questions to appropriate respondents.
    """
    __tablename__ = 'organizational_role'

    id = db.Column(db.Uuid, primary_key=True, default=generate_uuid)
    created_at = db.Column(db.DateTime, default=generate_timestamp)
    updated_at = db.Column(db.DateTime, default=generate_timestamp)

    name = db.Column(db.String, nullable=False)


# --- OrganizationMember and association table ---
class OrganizationMember(db.Model):
    """
    OrganizationMember – Represents a person affiliated with an organization who may participate in an audit or be assigned one or more roles.

    This entity allows us to associate real individuals with their respective roles (e.g., Jane Doe as both Data Engineer and Executive Leader)
    within a given organization. Members can be referenced when collecting responses, scheduling interviews, or tracking role accountability.

    Fields:
      - id: Unique identifier for the member (UUID).
      - name: Full name of the person (e.g., "Jane Doe").
      - email: Contact email address (must be unique).
      - slack_handle: Optional Slack username or identifier.
      - teams_handle: Optional Microsoft Teams handle.
      - created_at / updated_at: Timestamps for lifecycle tracking.

    Relationships:
      - roles: Many-to-many relationship to OrganizationalRole via an association table.
    """
    __tablename__ = 'organization_member'

    id = db.Column(db.Uuid, primary_key=True, default=generate_uuid)
    created_at = db.Column(db.DateTime, default=generate_timestamp)
    updated_at = db.Column(db.DateTime, default=generate_timestamp)

    organization_id = db.Column(db.Uuid, db.ForeignKey('organization.id'), nullable=False)

    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    slack_handle = db.Column(db.String, nullable=True)
    teams_handle = db.Column(db.String, nullable=True)

    roles = db.relationship(
        'OrganizationalRole',
        secondary='member_role_association',
        backref=db.backref('members', lazy=True)
    )

# Association table for many-to-many relationship between members and roles
member_role_association = db.Table(
    'member_role_association',
    db.Column('member_id', db.Uuid, db.ForeignKey('organization_member.id'), primary_key=True),
    db.Column('role_id', db.Uuid, db.ForeignKey('organizational_role.id'), primary_key=True)
)


class Practice(db.Model):
    """
    Practice – Represents a high-level domain or discipline under evaluation during an audit.

    Practices serve as the top-level structure in the audit hierarchy and typically include areas like:
      - Data Engineering
      - Product Analytics
      - Corporate Reporting
      - Marketing Analytics

    Each practice encompasses multiple aspects (PracticeAspect), which are more specific areas of focus within the domain.

    Fields:
      - id: Unique identifier for the practice (UUID).
      - name: Name of the practice (e.g., "Data Engineering").
      - created_at / updated_at: Timestamps for audit tracking and freshness.
      - practice_aspects: List of related aspects representing subdomains or components under this practice.

    Example:
      Practice(name="Product Analytics") could include aspects like:
        - Feature Adoption & Engagement
        - Retention & Churn Analysis
        - Experimentation & A/B Testing
    """
    __tablename__ = 'practice'

    id = db.Column(db.Uuid, primary_key=True, default=generate_uuid)
    created_at = db.Column(db.DateTime, default=generate_timestamp)
    updated_at = db.Column(db.DateTime, default=generate_timestamp)

    name = db.Column(db.String, nullable=False)

    practice_aspects = db.relationship('PracticeAspect', backref='practice_aspect', lazy=True)


class PracticeAspect(db.Model):
    """
    PracticeAspect – Represents a lower-level focus area within a broader practice, such as “Attribution Modeling” under “Marketing Analytics” or “Data Ingestion” under “Data Engineering”.

    Each practice aspect is uniquely identified and linked to a parent practice. It defines the domain-specific subcategory that guides assessment and evaluation.

    Fields:
      - id: Unique UUID for the practice aspect.
      - name: Descriptive name of the aspect (e.g., "Data Ingestion").
      - created_at / updated_at: Timestamps for audit tracking and change history.
      - practice_id: Foreign key linking this aspect to a parent Practice.

    Relationships:
      - capabilities: A list of AspectCapability objects that further decompose this aspect into measurable competencies.

    Example:
      A PracticeAspect with name="Retention & Churn Analysis" under practice="Product Analytics" might contain capabilities like:
        - "Cohort-based retention tracking"
        - "Churn signal identification"
    """
    __tablename__ = 'practice_aspect'

    id = db.Column(db.Uuid, primary_key=True, default=generate_uuid)
    created_at = db.Column(db.DateTime, default=generate_timestamp)
    updated_at = db.Column(db.DateTime, default=generate_timestamp)

    practice_id = db.Column(db.Uuid, db.ForeignKey('practice.id'), nullable=False)

    name = db.Column(db.String, nullable=False)
    objective=db.Column(db.String, nullable=True)
    activities =db.Column(db.String, nullable=True)


    capabilities = db.relationship('AspectCapability', backref='aspect_capability', lazy=True)


class AspectCapability(db.Model):
    """
    AspectCapability – Represents a specific competency or functional ability within a given PracticeAspect.

    A capability defines a particular domain of knowledge or execution required to perform tasks effectively in a focus
    area (aspect). A capability is the unit by which maturity is assessed and improved. Each capability belongs to a
    PracticeAspect and is linked to a parent Practice for reference.

    Each capability is assessed using qualitative prompts (questions) and evaluated using a maturity rubric (levels 1–5).

    Fields:
      - id: Unique UUID for the capability.
      - name: Human-readable name of the capability (e.g., "Churn Signal Identification").
      - practice_id: Foreign key to the parent Practice.
      - practice_aspect_id: Foreign key to the parent PracticeAspect.
      - created_at / updated_at: Timestamps for lifecycle tracking.
      - rubrics: Associated MaturityRubric entries for scoring.
      - qualitative_prompts: Qualitative questions used to assess maturity.

    Example:
      Capability(name="Cohort Retention Tracking") under PracticeAspect(name="Retention & Churn Analysis")
    """
    __tablename__ = 'aspect_capability'

    id = db.Column(db.Uuid, primary_key=True, default=generate_uuid)
    created_at = db.Column(db.DateTime, default=generate_timestamp)
    updated_at = db.Column(db.DateTime, default=generate_timestamp)

    practice_id = db.Column(db.Uuid, db.ForeignKey('practice.id'), nullable=False)
    practice_aspect_id = db.Column(db.Uuid, db.ForeignKey('practice_aspect.id'), nullable=False)

    name = db.Column(db.String, nullable=False)

    rubrics = db.relationship('MaturityRubric', backref='maturity_rubric', lazy=True)
    qualitative_prompts = db.relationship('QualitativePrompt', backref='reflective_prompt', lazy=True)



class MaturityRubric(db.Model):
    """
    MaturityRubric – Defines maturity scoring levels for a specific capability within a practice and aspect.

    Each rubric entry defines a specific maturity level (score from 1 to 5), including a label and description explaining the operational characteristics of that level.

    Fields:
      - score: An integer from 1 to 5 indicating the maturity level.
      - level_name: A short label summarizing the level (e.g., "Initial", "Developing", "Defined", "Managed", "Optimized").
      - state: A long-form description of the maturity state at this level.
      - capability_id: Foreign key to the capability being assessed.
      - aspect_id: Foreign key to the aspect containing the capability.
      - practice_id: Foreign key to the practice containing the aspect.

    Use:
      The rubric is used during audit assessments to evaluate current and target maturity levels for a given capability.
    """
    __tablename__ = 'maturity_rubric'

    id = db.Column(db.Uuid, primary_key=True, default=generate_uuid)
    created_at = db.Column(db.DateTime, default=generate_timestamp)
    updated_at = db.Column(db.DateTime, default=generate_timestamp)

    practice_id = db.Column(db.Uuid, db.ForeignKey('practice.id'), nullable=False)
    practice_aspect_id = db.Column(db.Uuid, db.ForeignKey('practice_aspect.id'), nullable=False)
    aspect_capability_id = db.Column(db.Uuid, db.ForeignKey('aspect_capability.id'), nullable=False)

    score = db.Column(db.Integer, nullable=False)
    level_name = db.Column(db.String, nullable=False)
    state = db.Column(db.Text, nullable=False)


class ReflectivePrompt(db.Model):
    """
    ReflectivePrompt – A single open-ended question designed to uncover the implicit maturity, culture, or process within a practice area or subject category.

    These prompts are used during audit interviews to encourage candid, qualitative responses that may uncover gaps,
    misalignments, or maturity opportunities. Reflective prompts do not directly map to scores, but rather provide
    narrative context and insights.

    Fields:
      - id: Unique identifier for the prompt.
      - practice_id: Foreign key reference to the associated high-level practice (e.g., Data Engineering).
      - practice_aspect_id: Foreign key reference to the associated practice aspect (e.g., Data Ingestion).
      - prompt: The actual question to pose to stakeholders.
      - insight_goal: A short statement describing what the response to the prompt is intended to uncover.
      - created_at / updated_at: Timestamps for versioning and data freshness.

    Example:
      Prompt: "What recent ingestion-related incident taught you the most?"
      Insight Goal: Reveals responsiveness and lessons learned from ingestion failures.
    """
    __tablename__ = 'reflective_prompt'

    id = db.Column(db.Uuid, primary_key=True, default=generate_uuid)
    created_at = db.Column(db.DateTime, default=generate_timestamp)
    updated_at = db.Column(db.DateTime, default=generate_timestamp)

    practice_id = db.Column(db.Uuid, db.ForeignKey('practice.id'), nullable=False)
    practice_aspect_id = db.Column(db.Uuid, db.ForeignKey('practice_aspect.id'), nullable=False)

    prompt = db.Column(db.String, nullable=False)
    insight_goal = db.Column(db.Text, nullable=False)



class QualitativePrompt(db.Model):
    """
    QualitativePrompt – A targeted, role-based question used to assess the maturity of a specific capability within a
    subject area and practice domain.

    This prompt is typically closed-ended or multiple-choice and is designed to elicit a response that can be mapped to a rubric-defined maturity level (1–5). Unlike reflective prompts, qualitative prompts are structured and
    evaluative.

    Fields:
      - id: Unique identifier for the prompt.
      - practice_id: Foreign key reference to the high-level domain (e.g., Data Engineering).
      - practice_aspect_id: Foreign key reference to the subject area (e.g., Data Ingestion).
      - aspect_capability_id: Foreign key reference to the specific capability being assessed.
      - prompt: The question text presented to the interviewee.
      - created_at / updated_at: Timestamps for auditing and version control.

    Example:
      Prompt: "Do you have a consistent event taxonomy that defines core user actions?"
    """
    __tablename__ = 'qualitative_prompt'

    id = db.Column(db.Uuid, primary_key=True, default=generate_uuid)
    created_at = db.Column(db.DateTime, default=generate_timestamp)
    updated_at = db.Column(db.DateTime, default=generate_timestamp)

    practice_id = db.Column(db.Uuid, db.ForeignKey('practice.id'), nullable=False)
    practice_aspect_id = db.Column(db.Uuid, db.ForeignKey('practice_aspect.id'), nullable=False)
    aspect_capability_id = db.Column(db.Uuid, db.ForeignKey('aspect_capability.id'), nullable=False)

    prompt = db.Column(db.String, nullable=False)



class AssessmentResponse(db.Model):
    __tablename__ = 'assessment_responses'

    id = db.Column(db.Uuid, primary_key=True, default=generate_uuid)
    created_at = db.Column(db.DateTime, default=generate_timestamp)
    updated_at = db.Column(db.DateTime, default=generate_timestamp)

    audit_effort_id = db.Column(db.Uuid, db.ForeignKey('audit_effort.id'), nullable=False)
    practice_id = db.Column(db.Uuid, db.ForeignKey('practice.id'), nullable=False)
    practice_aspect_id = db.Column(db.Uuid, db.ForeignKey('practice_aspect.id'), nullable=False)
    aspect_capability_id = db.Column(db.Uuid, db.ForeignKey('aspect_capability.id'), nullable=False)
    organizational_role_id = db.Column(db.Uuid, db.ForeignKey('organizational_role.id'), nullable=False)

    score = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    evidence = db.Column(db.Text)


class AuditEffort(db.Model):
    """
    AuditEffort – Represents a distinct audit engagement conducted for an organization.

    Each audit effort captures a point-in-time maturity assessment across a defined set of practices, aspects, and capabilities.
    Organizations may conduct multiple audits over time, which may be in 'draft' (work in progress) or 'certified'
    (finalized) status. Each audit effort may include qualitative and quantitative responses, evidence, improvement plans,
    and associated metadata.

    Fields:
      - id: Unique identifier (UUID) for the audit effort.
      - name: Name of the audit effort (e.g., "Q1 2025 Data Engineering Audit").
      - status: Current status of the audit (e.g., 'draft', 'certified').
      - auditor: Optional name or identifier of the person/team conducting the audit.
      - organization_id: Foreign key linking the audit effort to an Organization.
      - created_at / updated_at: Timestamps for lifecycle and versioning.
      - responses: Relationship to all AssessmentResponse records captured during this audit.

    Example:
      An audit effort titled "2024 Data Engineering Review" with status="draft" might contain:
        - Capability-level maturity scores
        - Role-based assessments
        - Supporting evidence and notes
    """
    __tablename__ = 'audit_effort'
    __table_args__ = (
        db.UniqueConstraint('organization_id', 'name', name='uq_org_audit_name'),
    )
    id = db.Column(db.Uuid, primary_key=True, default=generate_uuid)
    created_at = db.Column(db.DateTime, default=generate_timestamp)
    updated_at = db.Column(db.DateTime, default=generate_timestamp)

    organization_id = db.Column(db.Uuid, db.ForeignKey('organization.id'), nullable=False)

    name = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False, default='draft')  # draft or certified
    auditor = db.Column(db.String)

    responses = db.relationship('AssessmentResponse', backref='audit_effort', lazy=True)

