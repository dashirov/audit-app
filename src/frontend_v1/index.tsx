import { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectItem } from '@/components/ui/select';
import Rating from '@mui/material/Rating';

export default function AuditApp() {
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
        fetch('/practices').then(res => res.json()).then(setPractices);
    }, []);

    const searchOrg = async () => {
        const res = await fetch(`/organizations?name=${orgName}`);
        const data = await res.json();
        if (data && data.length > 0) setOrgId(data[0].id);
    };

    const createAudit = async () => {
        const res = await fetch('/audits', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ org_id: orgId })
        });
        const audit = await res.json();
        console.log('Created audit:', audit);
    };

    const fetchAspects = async (practiceId) => {
        setSelectedPractice(practiceId);
        const res = await fetch(`/practice_aspects/${practiceId}`);
        const data = await res.json();
        setAspects(data);
    };

    const handleRatingChange = (aspectId, newValue) => {
        setRatings({ ...ratings, [aspectId]: newValue });
    };

    return (
        <main className="p-6 space-y-6">
        <Card>
            <CardContent className="space-y-4">
        <h2 className="text-xl font-semibold">Find or Create Audit</h2>
    <Input placeholder="Organization Name" value={orgName} onChange={e => setOrgName(e.target.value)} />
    <Button onClick={searchOrg}>Search Organization</Button>
    {orgId && <Button onClick={createAudit}>Create Audit Effort</Button>}
    </CardContent>
    </Card>

    <Card>
    <CardContent className="space-y-4">
    <h2 className="text-xl font-semibold">Configure Scope</h2>
    <Select onValueChange={fetchAspects}>
        {practices.map(p => (
                <SelectItem key={p.id} value={p.id}>{p.name}</SelectItem>
    ))}
        </Select>

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
            <label>Maturity Level</label>
        <Select>
        {[1, 2, 3, 4, 5].map(score => (
            <SelectItem key={score} value={score}>{score}</SelectItem>
        ))}
            </Select>
            <Rating
            name={`rating-${a.id}`}
            value={ratings[a.id] || 0}
            onChange={(event, newValue) => handleRatingChange(a.id, newValue)}
            />
            </div>
            <Textarea placeholder="Narrative / Evidence" />
            </CardContent>
            </Card>
        ))}
        </main>
    );
    }
