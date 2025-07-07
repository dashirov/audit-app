import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router';
import { DataGridPremium } from '@mui/x-data-grid-premium/DataGridPremium';
import { Button, Modal, Box, TextField } from '@mui/material';

const baseURL = import.meta.env.VITE_API_BASE_URL;

export default function OrganizationsPage() {
    const [organizations, setOrganizations] = useState([]);
    const [openModal, setOpenModal] = useState(false);
    const [newOrgName, setNewOrgName] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        fetch(`${baseURL}/organizations`)
            .then(res => res.json())
            .then(data => setOrganizations(data));
    }, []);

    const handleCreateOrg = async () => {
        const res = await fetch(`${baseURL}/organizations`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: newOrgName }),
        });
        const org = await res.json();
        setOrganizations(prev => [...prev, org]);
        setOpenModal(false);
        setNewOrgName('');
        navigate(`/organizations/${org.id}`);
    };

    return (
        <div style={{ height: 600, width: '100%' }}>
            <Button variant="contained" onClick={() => setOpenModal(true)}>Create New Organization</Button>
            <DataGridPremium
                rows={organizations}
                columns={[
                    { field: 'name', headerName: 'Organization Name', width: 200 },
                    { field: 'latest_audit_name', headerName: 'Latest Audit', width: 200 },
                ]}
                getRowId={row => row.id}
                onRowClick={params => navigate(`/organizations/${params.row.id}`)}
            />
            <Modal open={openModal} onClose={() => setOpenModal(false)}>
                <Box sx={{ p: 4, backgroundColor: 'white', m: 'auto', mt: '10%', width: 400 }}>
                    <TextField
                        label="Organization Name"
                        fullWidth
                        value={newOrgName}
                        onChange={e => setNewOrgName(e.target.value)}
                    />
                    <Button onClick={handleCreateOrg} fullWidth sx={{ mt: 2 }}>Submit</Button>
                </Box>
            </Modal>
        </div>
    );
}