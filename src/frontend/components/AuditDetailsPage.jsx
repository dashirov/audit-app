import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Card, CardContent, Typography, Box } from '@mui/material';

export default function AuditDetailsPage() {
    const baseURL = import.meta.env.VITE_API_BASE_URL;

    const { organizationId,auditId } = useParams();

    const [audit, setAudit] = useState(null);
    const [practices, setPractices] = useState([]);
    const [roleMappings, setRoleMappings] = useState([]);
    const [members, setMembers] = useState([]);

    useEffect(() => {
        // Fetch audit details
        fetch(`${baseURL}/audits/${auditId}`).then(res => res.json()).then(setAudit);

        // Fetch other supporting data
        fetch(`${baseURL}/practices`).then(res => res.json()).then(setPractices);
        fetch(`${baseURL}/organizational_roles`).then(res => res.json()).then(setRoleMappings);
        fetch(`${baseURL}/organizations/${organizationId}/members`).then(res => res.json()).then(setMembers);
    }, [auditId]);

    return (
        <Box p={3}>
            <Typography variant="h4" gutterBottom>
                Audit Configuration
            </Typography>

            <Card>
                <CardContent>
                    <Typography variant="h6">1. Select Practices to Audit</Typography>
                    {/* Practice selection component */}
                </CardContent>
            </Card>

            <Card>
                <CardContent>
                    <Typography variant="h6">2. Assign Qualitative Prompts to Roles</Typography>
                    {/* UI to assign qualitative prompts */}
                </CardContent>
            </Card>

            <Card>
                <CardContent>
                    <Typography variant="h6">3. Assign Reflective Prompts to Roles</Typography>
                    {/* UI to assign reflective prompts */}
                </CardContent>
            </Card>

            <Card>
                <CardContent>
                    <Typography variant="h6">4. Select Which Members to Prompt</Typography>
                    {/* List of members with toggles for inclusion */}
                </CardContent>
            </Card>
        </Box>
    );
}