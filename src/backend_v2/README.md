# Audit Maturity Assessment App

This application supports organizational maturity assessments across areas like Product Analytics, Business Intelligence, Corporate Reporting, and AI Enablement. It provides a structured interface for evaluators to assess current practices, capture evidence, and define improvement roadmaps.

## Business Requirements

### Entities and Relationships

1. **Organization** – Each audit is associated with a specific organization.
2. **OrganizationalRole** – The roles various employees play in an organization (e.g., Member of the Board).
3. **OrganizationMember** – Specific individuals associated with the organization who play one or more organizational roles (e.g., Jane Doe <jane.doe@example.com> plays roles such as Data Engineer, Marketing Analyst, and Executive).
4. **Practice** – High-level focus areas such as Product Analytics, Corporate Reporting.
5. **PracticeAspect** – Finer-grained categories under each practice (e.g., Feature Adoption).
6. **AspectCapability** – Represents a specific competency or functional ability within a given Practice Aspect.
7. **AuditEffort** – Each organization can have multiple audits (draft, certified).
8. **AssessmentResponse** – Maturity score, notes, and evidence captured for each audit.
9. **Autosave and Versioning** – Changes are automatically saved and can be rolled back.

## Features

- Organization onboarding and audit tracking
- Subject area/category selection with scoring via rubric (1–5)
- Role-based interview mode with answer mapping
- Evidence collection and narrative capture
- Improvement plan definition with future target setting
- Reorderable categories to reflect priority
- Autosave and undo functionality
- PostgreSQL persistence

## Tech Stack

- **Backend**: Flask, SQLAlchemy, PostgreSQL
- **Frontend**: Vanilla JavaScript, HTML/CSS
- **Containerized**: Docker, Docker Compose
- **Testing**: Pytest

## Setup Instructions

### 1. Clone and configure environment

```bash
git clone https://github.com/your-org/audit-app.git
cd audit-app
cp .env.example .env
```

### 2. Build and run with Docker Compose

```bash
docker-compose up --build
```

Ensure your `.env` contains a valid `DATABASE_URL` like:

```
DATABASE_URL=postgresql://username:password@host.docker.internal:5432/audit
```

### 3. Run Tests

```bash
pytest tests/
```

## API Overview

- `GET /organizations`
- `POST /audits`
- `GET /subject-areas`, `/categories`, `/roles`
- `GET /questions?category_id=&role_id=`
- `POST /responses`
- `POST /responses/undo`

## License

MIT License

## API Endpoints and Example Usage

### Organizations

- `GET /organizations`  
  List all organizations.

- `GET /organizations/<uuid>`  
  Retrieve a specific organization by ID.

- `GET /organizations/by-name/<name>`  
  Retrieve an organization by name.

- `POST /organizations`  
  Create a new organization.  
  **Request Body:**
  ```json
  {
    "name": "ACME Corp."
  }
  ```

### Organization Members

- `POST /organization-members`  
  Add a member to an organization and assign roles.  
  **Request Body:**
  ```json
  {
    "org_id": "organization-uuid",
    "name": "Jane Doe",
    "email": "jane.doe@example.com",
    "slack": "@janedoe",
    "teams": "janedoe@teams.com",
    "roles": ["role-uuid-1", "role-uuid-2"]
  }
  ```

### Audit Efforts

- `POST /audits`  
  Create a new audit effort for an organization.  
  **Request Body:**
  ```json
  {
    "org_id": "organization-uuid"
  }
  ```

### Practices

- `GET /practices`  
  List all practices.

- `GET /practice_aspects/<practice_id>`  
  List practice aspects for a given practice.

- `GET /aspect_capabilities/<aspect_id>`  
  List capabilities for a given practice aspect.

### Roles

- `GET /roles`  
  Retrieve all organizational roles.

### Interview Questions

- `GET /questions?category_id=<uuid>&role_id=<uuid>`  
  Retrieve interview questions for a specific subject category and role.

### Assessment Responses

- `POST /responses`  
  Submit or autosave an assessment response.  
  **Request Body:**
  ```json
  {
    "audit_id": "audit-effort-uuid",
    "category_id": "category-uuid",
    "role_id": "role-uuid",
    "score": 4,
    "notes": "Validated using clickstream.",
    "evidence": "dashboard-screenshot.pdf"
  }
  ```

- `POST /responses/undo`  
  Roll back the most recent assessment response.  
  **Request Body:**
  ```json
  {
    "audit_id": "audit-effort-uuid",
    "category_id": "category-uuid",
    "role_id": "role-uuid"
  }
  ```

## Authentication

Currently, all API endpoints are open for testing. Production deployment should include proper authentication and access control.