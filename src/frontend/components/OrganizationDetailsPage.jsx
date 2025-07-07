import {useEffect, useState} from 'react';
import {useParams} from 'react-router';
import { useNavigate } from 'react-router-dom';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import {DataGridPremium} from '@mui/x-data-grid-premium/DataGridPremium';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogActions from '@mui/material/DialogActions';
import Alert from '@mui/material/Alert';
import TextField from '@mui/material/TextField';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import Checkbox from '@mui/material/Checkbox';
import ListItemText from '@mui/material/ListItemText';
import {Chip} from '@mui/material';

const baseURL = import.meta.env.VITE_API_BASE_URL;

export default function OrganizationDetailsPage() {
    const {organizationId} = useParams();
    const navigate = useNavigate();
    const [organization, setOrganization] = useState(null);
    const [audits, setAudits] = useState([]);
    const [showAuditModal, setShowAuditModal] = useState(false);
    const [members, setMembers] = useState([]);
    const [showMemberModal, setShowMemberModal] = useState(false);
    const [selectedMember, setSelectedMember] = useState(null);
    const [organizationalRoles, setOrganizationalRoles] = useState([]);
    // For legacy modal, kept for now, but will use newAuditName for new audit creation
    const [newAudit, setNewAudit] = useState({
        name: '',
        status: 'draft',
        auditor: ''
    });
    const [newMember, setNewMember] = useState({
        name: '',
        email: '',
        slack_handle: '',
        teams_handle: '',
        role_ids: []
    });
    // New states for the improved audit creation flow
    const [newAuditName, setNewAuditName] = useState('');
    const [error, setError] = useState('');
    const [showDraftDialog, setShowDraftDialog] = useState(false);
    const [existingDraft, setExistingDraft] = useState(null);

    const handleAuditRowClick = (params) => {
        navigate(`/organizations/${organizationId}/audits/${params.row.id}`);
    };
    useEffect(() => {
        fetch(`${baseURL}/organizations/${organizationId}`)
            .then(res => res.json())
            .then(setOrganization);

        fetch(`${baseURL}/organizations/${organizationId}/audits`)
            .then(res => res.json())
            .then(setAudits);

        fetch(`${baseURL}/organizations/${organizationId}/members`)
            .then(res => res.json())
            .then(setMembers);

        fetch(`${baseURL}/organizational_roles`)
            .then(res => res.json())
            .then(setOrganizationalRoles);

    }, [organizationId]);


    const createMember = async () => {
        // orgId is the current organization's ID (organizationId from useParams)
        // memberData is the payload for the new member (newMember)
        const res = await fetch(`${baseURL}/organizations/${organizationId}/members`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(newMember),
        });
        if (res.ok) {
            await fetchMembers();
            setShowMemberModal(false);
            setSelectedMember(null);
            setNewMember({
                name: '',
                email: '',
                slack_handle: '',
                teams_handle: '',
                role_ids: []
            });
        }
    };

    // Delete member handler for modal
    // Ensure this is in OrganizationDetailsPage's scope
    const handleDeleteMember = async (memberId) => {
        try {
            const response = await fetch(`${baseURL}/organizations/${organizationId}/members/${memberId}`, {
                method: 'DELETE'
            });
            if (response.ok) {
                setMembers(members.filter((m) => m.id !== memberId));
                setShowMemberModal(false); // close modal
                setNewMember({
                    name: '',
                    email: '',
                    slack_handle: '',
                    teams_handle: '',
                    role_ids: []
                });
            } else {
                console.error('Failed to delete member');
            }
        } catch (error) {
            console.error('Error deleting member:', error);
        }
    };

    const createOrEditMember = async () => {
        // If editing (member has an id), send PUT, else POST
        let url, method;
        if (newMember.id) {
            url = `${baseURL}/organizations/${organizationId}/members/${newMember.id}`;
            method = 'PUT';
        } else {
            url = `${baseURL}/organizations/${organizationId}/members`;
            method = 'POST';
        }
        const res = await fetch(url, {
            method,
            headers: {'Content-Type': 'application/json'},

            body: JSON.stringify(newMember),
        });
        if (res.ok) {
            await fetchMembers();
            setShowMemberModal(false);
            setSelectedMember(null);
            setNewMember({
                name: '',
                email: '',
                slack_handle: '',
                teams_handle: '',
                role_ids: []
            });
        }
    };


    // Handler for editing a member (row click)
    const handleEditMember = (params) => {
        setSelectedMember(params.row);
        setNewMember({
            id: params.row.id, // This ensures update path is triggered
            name: params.row.name || '',
            email: params.row.email || '',
            slack_handle: params.row.slack_handle || '',
            teams_handle: params.row.teams_handle || '',
            role_ids: params.row.role_ids || [],
        });
        setShowMemberModal(true);
    };

    // New audit creation logic
    const handleCreateAudit = async () => {
        setError('');
        try {
            const response = await fetch(`${baseURL}/organizations/${organizationId}/audits`);
            const auditsList = await response.json();
            const duplicate = auditsList.find(a => a.name === newAuditName);
            if (duplicate) {
                setError("An audit with this name already exists.");
                return;
            }
            const draft = auditsList.find(a => a.status === 'draft');
            if (draft) {
                setExistingDraft(draft);
                setShowDraftDialog(true);
                return;
            }
            proceedToCreateNewAudit();
        } catch (e) {
            setError("Failed to create audit.");
        }
    };

    const proceedToCreateNewAudit = async () => {
        setError('');
        try {
            const res = await fetch(`${baseURL}/audits`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({org_id: organizationId, name: newAuditName})
            });
            if (res.ok) {
                const audit = await res.json();
                setAudits([...audits, audit]);
                setShowAuditModal(false);
                setNewAuditName('');
                // Optionally, navigate to the audit or show a success message
            } else {
                setError("Failed to create audit.");
            }
        } catch (e) {
            setError("Failed to create audit.");
        }
    };

    const navigateToDraft = (auditId) => {
        // Implement route redirection logic if needed
        // For now, just log
        console.log("Navigating to draft audit:", auditId);
        setShowDraftDialog(false);
    };

    const fetchMembers = async () => {
        fetch(`${baseURL}/organizations/${organizationId}/members`)
            .then(res => res.json())
            .then(setMembers);
    };


    return (
        <main className="p-6 space-y-6">
            <h2 className="text-2xl font-semibold">{organization?.name} Details</h2>

            <Card sx={{marginBottom: 2}}>
                <CardContent>
                    <h3 style={{fontSize: '1.25rem', fontWeight: 600, marginBottom: 16}}>Audit Efforts</h3>
                    <Button variant="contained" onClick={() => setShowAuditModal(true)}>Create New Audit</Button>
                    <DataGridPremium
                        rows={audits}
                        columns={[
                            {field: 'name', headerName: 'Audit ID', width: 250},
                            {field: 'created_at', headerName: 'Created Date', width: 200},
                            {field: 'status', headerName: 'Status', width: 100}
                        ]}
                        getRowId={(row) => row.id}
                        autoHeight
                        onRowClick={handleAuditRowClick}
                    />
                </CardContent>
            </Card>

            {/* Error Alert for audit creation */}
            {error && <Alert severity="error" sx={{mb: 2}}>{error}</Alert>}

            {/* Dialog for existing draft audit */}
            <Dialog open={showDraftDialog} onClose={() => setShowDraftDialog(false)}>
                <DialogTitle>Continue Existing Draft?</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        There is already a draft audit in progress. Would you like to continue working on it or start a
                        new one?
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => navigateToDraft(existingDraft?.id)}>Continue Draft</Button>
                    <Button onClick={() => {
                        setShowDraftDialog(false);
                        proceedToCreateNewAudit();
                    }} color="primary">Start New Audit</Button>
                </DialogActions>
            </Dialog>

            <Dialog open={showAuditModal} onClose={() => setShowAuditModal(false)}>
                <DialogTitle>Launch new audit effort</DialogTitle>
                <DialogContent className="space-y-4">
                    {/* Error Alert for audit creation (inside modal for context) */}
                    {error && <Alert severity="error" sx={{mb: 2}}>{error}</Alert>}
                    <TextField
                        label="Audit Name"
                        fullWidth
                        value={newAuditName}
                        onChange={e => setNewAuditName(e.target.value)}
                        autoFocus
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setShowAuditModal(false)}>Cancel</Button>
                    <Button onClick={handleCreateAudit} variant="contained">Save</Button>
                </DialogActions>
            </Dialog>

            <Card sx={{marginBottom: 2}}>
                <CardContent>
                    <h3 style={{fontSize: '1.25rem', fontWeight: 600, marginBottom: 16}}>Organization Members</h3>
                    <Button
                        variant="contained"
                        onClick={() => {
                            setShowMemberModal(true);
                            setSelectedMember(null);
                            setNewMember({
                                name: '',
                                email: '',
                                slack_handle: '',
                                teams_handle: '',
                                role_ids: []
                            });
                        }}
                    >
                        Add Member
                    </Button>
                    <DataGridPremium
                        rows={members}
                        columns={[
                            {field: 'name', headerName: 'Name', width: 200},
                            {field: 'email', headerName: 'Email', width: 250},
                            {field: 'slack_handle', headerName: 'Slack', width: 150},
                            {field: 'teams_handle', headerName: 'Teams', width: 150},
                            {
                                field: 'role_names',
                                headerName: 'Roles',
                                width: 300,
                                renderCell: (params) => (
                                    <div style={{display: 'flex', flexWrap: 'wrap', gap: 4}}>
                                        {(params.row.role_names || []).map((role, idx) => (
                                            <Chip key={idx} label={role} size="small"/>
                                        ))}
                                    </div>
                                )
                            }
                        ]}
                        getRowId={(row) => row.id}
                        autoHeight
                        onRowClick={handleEditMember}
                    />
                </CardContent>
            </Card>


            <Dialog open={showMemberModal} onClose={() => {
                setShowMemberModal(false);
                setSelectedMember(null);
            }}>
                <DialogTitle>
                    {selectedMember ? 'Edit Organization Member' : 'Add Organization Member'}
                </DialogTitle>
                <DialogContent className="space-y-4">
                    <TextField
                        label="Name"
                        fullWidth
                        value={newMember.name}
                        onChange={e => setNewMember({...newMember, name: e.target.value})}
                    />
                    <TextField
                        label="Email"
                        fullWidth
                        value={newMember.email}
                        onChange={e => setNewMember({...newMember, email: e.target.value})}
                    />
                    <TextField
                        label="Slack"
                        fullWidth
                        value={newMember.slack_handle}
                        onChange={e => setNewMember({...newMember, slack_handle: e.target.value})}
                    />
                    <TextField
                        label="Teams"
                        fullWidth
                        value={newMember.teams_handle}
                        onChange={e => setNewMember({...newMember, teams_handle: e.target.value})}
                    />
                    <FormControl fullWidth>
                        <InputLabel id="roles-label">Roles</InputLabel>
                        <Select
                            labelId="roles-label"
                            multiple
                            value={newMember.role_ids}
                            onChange={(e) => setNewMember({...newMember, role_ids: e.target.value})}
                            renderValue={(selected) =>
                                organizationalRoles
                                    .filter((role) => selected.includes(role.id))
                                    .map((role) => role.name)
                                    .join(', ')
                            }
                        >
                            {organizationalRoles.map((role) => (
                                <MenuItem key={role.id} value={role.id}>
                                    <Checkbox checked={newMember.role_ids.includes(role.id)}/>
                                    <ListItemText primary={role.name}/>
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => {
                        setShowMemberModal(false);
                        setSelectedMember(null);
                    }}>Cancel</Button>
                    <Button onClick={createOrEditMember} variant="contained">Save</Button>
                    {newMember.id && (
                        <Button
                            variant="outlined"
                            color="error"
                            onClick={() => handleDeleteMember(newMember.id)}
                        >
                            Delete
                        </Button>
                    )}
                </DialogActions>
            </Dialog>
        </main>
    );
}

