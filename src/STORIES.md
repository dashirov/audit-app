## User Experience Stories

### 1. Organizations Management

Find Organization by Name

* **Story:** As a consultant conducting a maturity assessment, I want to find an existing organization record by its name, so that I can begin setting up the audit effort for that organization.

View List of Organizations

* **Story:** As a consultant or user opening the web application, I want to see a list of organizations and their most recent audit effort in a searchable table, so that I can locate and navigate to relevant organization data easily.

Create New Organization

* **Story:** As a consultant or administrator, I want to be able to create a new organization record via a modal form if the organization I’m looking for does not yet exist, so that I can proceed to structure and perform audits on it.

Navigate to Organization Details

* **Story:** As a user, I want to click on a listed organization and view its details (audits and members), so that I can manage or initiate assessments for that organization.

View and Create Organization Members
* **Story:** As a consultant conducting a maturity assessment, I want to add members of the organization to an existing organization, so that they can participate in interviews and responses as part of the audit.

View and Create Audit Efforts for Organization
* **Story:** As a consultant, I want to view past audit efforts and initiate new audit efforts for a given organization, so that I can ensure historical continuity and perform up-to-date assessments.

### 2. Manage Organizations and Members


* **Story:** As a consultant conducting a maturity assessment,
I want to view a searchable table of all organizations along with their latest audits,
so that I can quickly locate or verify the status of any organization.


* **Story:** As a consultant,
I want to create a new organization via a modal dialog if it does not already exist,
so that I can initiate a new audit effort without leaving the context of the organization listing screen.


* **Story:** As a consultant,
I want to access the detail page for an organization,
so that I can manage its audits and organizational members in one place.


* **Story:** As a consultant,
I want to view a list of all members of a given organization,
so that I can understand who participates in the assessment process.


* **Story:** As a consultant,
I want to add a new member to the organization via a form,
so that I can configure audit participants and assign relevant roles.


* **Story:** As a consultant,
I want to assign one or more roles to each organization member,
so that the assessment reflects real organizational structure.


* **Story:** As a consultant,
I want to see member roles displayed clearly in the members table,
so that I can understand the distribution of responsibilities at a glance.


### 3. Audit Effort Creation and Validation


* **Story:** As a consultant,
I want to create a new audit effort only if no existing draft is in progress,
so that I avoid duplicate or overlapping efforts unintentionally.


* **Story:** As a consultant,
I want to be prompted to continue an existing draft instead of creating a new one,
so that I preserve work-in-progress and avoid fragmentation.


* **Story:** As a consultant,
I want to assign a unique name to each audit effort under the same organization,
so that audit efforts are clearly distinguishable in records.


### 4. Application Behavior and API Integration

* **Story:** As a frontend user,
I want the app to automatically refresh the organization members table when a new member is added,
so that I immediately see changes without needing to reload the page.


* **Story:** As a frontend developer,
I want the app to display error messages if API routes return invalid or incomplete responses,
so that I can troubleshoot and resolve integration issues quickly.


* **Story:** As a frontend developer,
I want to use Material UI components like DataGridPremium, Select, Rating, and AppBar,
so that the application maintains a consistent and professional look-and-feel.

### 5. Create New Audit Effort

* **Story:** As a consultant, I want to create a new audit effort for a selected organization, so that I can initiate the assessment process and begin capturing data.

### 6. View and Select Practice Areas

* **Story:** As a consultant preparing for the assessment, I want to view available practices and finer-grain aspects of the practice, so that I can structure my audit effort appropriately.

### 7. Configure Audit Scope


* **Story:** As a consultant preparing for the assessment, I want to update the audit configuration with the selection of some of the available practices and finer-grain aspects of the practice I will be assessing, so that I can structure my audit effort appropriately.


* **Story:** As a consultant preparing for the assessment, I want to select specific organizational users and assign them reflective and/or qualitative prompts to respond to, so that I can structure my audit effort appropriately.


### 8. Interview Preparation

* **Story:** As a consultant, I want to view interview questions filtered by subject category and role, so that I can prepare for conversations with relevant stakeholders.

### 9. Capture Responses

* **Story:** As a consultant, I want to submit and autosave assessment responses (score, notes, evidence), so that progress is preserved and versioned safely.

### 10. Undo Recent Changes

* **Story:** As a consultant, I want to undo the most recent assessment response, so that I can correct errors or update outdated input.

### 11. Define Improvement Plan

* **Story:** As a consultant, I want to set maturity targets and write narratives for improvement plans, so that the organization can work toward higher capability levels.

### 12. Reorder Priorities

* **Story:** As a consultant, I want to reorder subject categories to indicate their strategic priority, so that improvement efforts are properly focused.

### 13. Manage Organization Members

* **Story:** As a consultant or admin, I want to register organization members and assign them roles, so that interview responsibilities and perspectives are accurately represented.

### 14. Review and Certify Audit Results

* **Story:** As a consultant or organizational leader, I want to review all collected data and certify the audit, so that the assessment is finalized and available for stakeholders.

### 15. Generate Certified Report
* **Story:** As a consultant or organizational leader, I want to retrieve a certified document with the audit findings and an improvement plan, so that the finalized assessment results are presented to the stakeholders.

### 16. Navigation and Metadata Management

Global Navigation Menu for Metadata Management

* **Story:** As a consultant conducting a maturity assessment, I want to be able to access various aspects of managing relevant metadata from a menu common to all screens, so I can navigate to different screens quickly and intuitively.

### 17. Edit Organization Members

* **Story** As a consultant managing organization members,
I want to click on a row in the members table to open a pre-filled modal,
so that I can quickly edit a member’s information using the same interface I use to create new members.

### 18. Organization and Member Management

Story:
As a consultant or admin, I want to view a list of organizations and their most recent audit efforts on the landing page, so that I can quickly navigate to relevant audit work.

Story:
As a consultant, I want to create a new organization using a modal form, so that I can onboard a new client organization efficiently.

Story:
As a consultant, I want to view a table of all audit efforts for a selected organization, so that I can track historical and ongoing assessments.

Story:
As a consultant, I want to add new members to an organization by entering their details and assigning multiple organizational roles, so that they can participate in audit interviews.

Story:
As a consultant, I want to edit or delete an existing organizational member using a modal form, so that I can keep personnel records up to date.

Story:
As a consultant, I want to see organizational member roles represented in the members table, so I can understand responsibilities at a glance.

### 19. Audit Setup & Navigation

Story:
As a consultant, I want to click on an audit row and navigate to an Audit Details page, so I can configure that audit further.

Story:
As a consultant preparing for the assessment, I want to configure the audit by selecting practices and assigning qualitative and reflective prompts to roles, so that the scope and depth of the audit match our goals.

Story:
As a consultant preparing for the assessment, I want to select which organizational members will receive prompts or be excluded from the audit, so that participation is role-appropriate and efficient.

Story:
As a consultant, I want to be warned if I attempt to create a new audit when a draft audit already exists, so that I avoid duplicating effort or creating inconsistent audit records.

Story:
As a consultant, I want to ensure that audit effort names are unique within an organization, so that we can distinguish between different assessments clearly.

### 20. System UX & Routing

Story:
As a user, I want to navigate between different sections of the app (e.g., Organizations, Audits, Metadata) using a global navigation menu, so that I can move through the system easily.