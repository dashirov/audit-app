import {useState, useEffect} from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import TextareaAutosize from '@mui/material/TextareaAutosize';
import Rating from '@mui/material/Rating';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { Link }  from 'react-router';

export default function AuditApp() {
    // Set baseURL from environment variable, fallback to empty string
    const BASE_URL = import.meta.env.VITE_API_BASE_URL || '';
    const [orgName, setOrgName] = useState('');
    const [orgId, setOrgId] = useState(null);
    const [practices, setPractices] = useState([]);
    const [selectedPractice, setSelectedPractice] = useState(null);
    const [aspects, setAspects] = useState([]);
    const [selectedAspects, setSelectedAspects] = useState([]);
    const [members, setMembers] = useState([]);
    const [prompts, setPrompts] = useState([]);
    const [ratings, setRatings] = useState({});


    useEffect(() => {
        fetch(`${BASE_URL}/practices`).then(res => res.json()).then(setPractices);
    }, [BASE_URL]);

    const searchOrg = async () => {
        const res = await fetch(`${BASE_URL}/organizations?name=${orgName}`);
        const data = await res.json();
        if (data && data.length > 0) setOrgId(data[0].id);
    };




    const createAudit = async () => {
        const res = await fetch(`${BASE_URL}/audits`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({org_id: orgId})
        });
        const audit = await res.json();
        console.log('Created audit:', audit);
    };

    const fetchAspects = async (practiceId) => {
        setSelectedPractice(practiceId);
        const res = await fetch(`${BASE_URL}/practice_aspects/${practiceId}`);
        const data = await res.json();
        setAspects(data);
    };

    const handleRatingChange = (aspectId, newValue) => {
        setRatings({...ratings, [aspectId]: newValue});
    };

    return (
        <main className="p-6 space-y-6">
            <Link to="/organizations">
                View All Organizations
            </Link>
            <Card>
                <CardContent className="space-y-4">
                    <h2 className="text-xl font-semibold">Find or Create Audit</h2>
                    <TextField placeholder="Organization Name" value={orgName}
                               onChange={e => setOrgName(e.target.value)}/>
                    <Button onClick={searchOrg}>Search Organization</Button>
                    {orgId && <Button onClick={createAudit}>Create Audit Effort</Button>}
                </CardContent>
            </Card>

            <Card>
                <CardContent className="space-y-4">
                    <h2 className="text-xl font-semibold">Configure Scope</h2>
                    <FormControl fullWidth>
                        <InputLabel id="practice-select-label">Select Practice</InputLabel>
                        <Select
                            labelId="practice-select-label"
                            value={selectedPractice || ''}
                            label="Select Practice"
                            onChange={(e) => fetchAspects(e.target.value)}
                        >
                            {practices.map((p) => (
                                <MenuItem key={p.id} value={p.id}>{p.name}</MenuItem>
                            ))}
                        </Select>
                    </FormControl>

                    {aspects.map(a => (
                        <div key={a.id} className="flex items-center justify-between">
                            <span>{a.name}</span>
                            <Button onClick={() => setSelectedAspects([...selectedAspects, a])}>Add</Button>
                        </div>
                    ))}
                </CardContent>
            </Card>

            {selectedAspects.map(a => (
                <Card key={a.id}>
                    <CardContent className="space-y-2">
                        <h3 className="font-medium">{a.name}</h3>
                        <div className="flex space-x-4 items-center">
                            <FormControl>
                                <InputLabel id={`maturity-level-${a.id}`}>Maturity Level</InputLabel>
                                <Select
                                    labelId={`maturity-level-${a.id}`}
                                    defaultValue=""
                                    label="Maturity Level"
                                >
                                    {[1, 2, 3, 4, 5].map(score => (
                                        <MenuItem key={score} value={score}>{score}</MenuItem>
                                    ))}
                                </Select>
                            </FormControl>
                            <Rating
                                name={`rating-${a.id}`}
                                value={ratings[a.id] || 0}
                                onChange={(event, newValue) => handleRatingChange(a.id, newValue)}
                            />
                        </div>
                        <TextareaAutosize placeholder="Narrative / Evidence"/>
                    </CardContent>
                </Card>
            ))}
        </main>
    );
}
