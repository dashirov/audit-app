import pytest
from app import create_app
from config import TestingConfig
from models import db
from models.core import Organization, Practice, PracticeAspect,AspectCapability, OrganizationalRole, AuditEffort, OrganizationMember

@pytest.fixture
def app_and_client():
    app = create_app(config_class=TestingConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            org = Organization(name="Test Org")
            db.session.add(org)
            db.session.commit()

            practice = Practice(name="Data Engineering")
            db.session.add(practice)
            db.session.commit()

            practice_aspect = PracticeAspect(
                                      practice_id=practice.id

                                    , name="Data Ingestion"
                                    , objective="Extract data from diverse sources efficiently and reliably"
                                    , activities = str.join("\n",["- Implement batch and streaming data ingestion",
                                                      "- Use standardized connectors for sources (e.g., Kafka, S3, APIs)",
                                                      "- Enable retry mechanisms and dead-letter queues",
                                                      "- Monitor ingestion latency and error rates"])
                                    )
            db.session.add(practice_aspect)
            db.session.commit()

            aspect_capability = AspectCapability(
                practice_id=practice.id,
                practice_aspect_id=practice_aspect.id,
                name="Change Data Capture (CDC) & Incremental Load"
            )
            db.session.add(aspect_capability)
            db.session.commit()


            role = OrganizationalRole(name="Data Engineer")
            db.session.add(role)


            audit = AuditEffort(organization_id=org.id, name="2024 Audit")
            db.session.add(audit)

            db.session.commit()
        yield app, client

def test_get_organizations(app_and_client):
    """Test retrieval of all organizations."""
    _, client = app_and_client
    res = client.get("/organizations")
    assert res.status_code == 200
    assert len(res.get_json()) >= 1


# Test: get organization by id
def test_get_organization_by_id(app_and_client):
    """Test retrieval of a single organization by ID."""
    app, client = app_and_client
    with app.app_context():
        org = Organization.query.first()
        res = client.get(f"/organizations/{org.id}")
        assert res.status_code == 200
        json_data = res.get_json()
        assert json_data["id"] == str(org.id)
        assert json_data["name"] == org.name


# Test: get organization by name as query param
def test_get_organization_by_name(app_and_client):
    """Test retrieval of organizations filtered by name."""
    app, client = app_and_client
    with app.app_context():
        org = Organization.query.first()
        res = client.get(f"/organizations?name={org.name}")
        assert res.status_code == 200
        json_data = res.get_json()
        assert isinstance(json_data, list)
        assert any(o["name"] == org.name for o in json_data)

def test_organization_from_dict_and_list():
    """Test Organization.from_dict and Organization.from_list methods."""
    sample_data = {
        "id": "test-uuid",
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-02T00:00:00Z",
        "name": "Example Org"
    }

    # Test from_dict
    org = Organization.from_dict(sample_data)
    assert isinstance(org, Organization)
    assert org.id == "test-uuid"
    assert org.name == "Example Org"

    # Test from_list
    data_list = [sample_data, {**sample_data, "id": "another-uuid", "name": "Another Org"}]
    org_list = Organization.from_list(data_list)
    assert isinstance(org_list, list)
    assert all(isinstance(o, Organization) for o in org_list)
    assert org_list[0].id == "test-uuid"
    assert org_list[1].name == "Another Org"

def test_create_organization(app_and_client):
    """Test creation of a new organization."""
    _, client = app_and_client
    res = client.post("/organizations", json={ "name": "New Org" })
    assert res.status_code == 200
    assert "id" in res.get_json()

def test_create_audit(app_and_client):
    """Test creation of a new audit for an organization."""
    app, client = app_and_client
    with app.app_context():
        org = Organization.query.first()
        res = client.post("/audits", json={
            "org_id": str(org.id),
            "name": "Test Audit Effort"
        })
        assert res.status_code == 200
        json_data = res.get_json()
        assert "id" in json_data
        assert json_data["name"] == "Test Audit Effort"
        assert json_data["org_id"] == str(org.id)

def test_get_practices(app_and_client):
    """Test retrieval of subject areas."""
    _, client = app_and_client
    res = client.get("/practices")
    assert res.status_code == 200
    assert len(res.get_json()) >= 1

# Test: create organization member
def test_create_organization_member(app_and_client):
    """Test creation of an organization member with assigned roles."""
    app, client = app_and_client
    with app.app_context():
        org = Organization.query.first()
        role = OrganizationalRole.query.first()

        payload = {
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "slack_handle": "@jane",
            "teams_handle": "jane_teams",
            "role_ids": [str(role.id)]
        }

        res = client.post(f"/organizations/{org.id}/members", json=payload)
        assert res.status_code == 200
        json_data = res.get_json()
        assert "member_id" in json_data
        assert isinstance(json_data["member_id"], str)

def test_get_roles(app_and_client):
    """Test retrieval of all organizational roles."""
    _, client = app_and_client
    res = client.get("/roles")
    assert res.status_code == 200
    assert len(res.get_json()) >= 1


# Additional tests for practice aspects and aspect capabilities endpoints
def test_get_practice_aspects_by_practice_id(app_and_client):
    """Test retrieval of practice aspects by practice ID."""
    app, client = app_and_client
    with app.app_context():
        practice = Practice.query.first()
        res = client.get(f"/practice_aspects/{practice.id}")
        assert res.status_code == 200
        json_data = res.get_json()
        assert isinstance(json_data, list)
        assert any("name" in aspect for aspect in json_data)


def test_get_aspect_capabilities_by_aspect_id(app_and_client):
    """Test retrieval of aspect capabilities by aspect ID."""
    app, client = app_and_client
    with app.app_context():
        aspect = PracticeAspect.query.first()
        res = client.get(f"/aspect_capabilities/{aspect.id}")
        assert res.status_code == 200
        json_data = res.get_json()
        assert isinstance(json_data, list)
        assert any("name" in capability for capability in json_data)
