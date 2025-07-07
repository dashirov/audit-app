import { Routes, Route } from 'react-router-dom';
import GlobalMenu from './components/GlobalMenu';
import OrganizationsPage from './components/OrganizationsPage';
import OrganizationDetailsPage from './components/OrganizationDetailsPage';
import AuditDetailsPage from "./components/AuditDetailsPage";

export default function App() {
    return (
        <>
            <GlobalMenu />
            <Routes>
                <Route path="/" element={<OrganizationsPage />} />
                <Route path="/organizations/:organizationId" element={<OrganizationDetailsPage />} />
                <Route path="/organizations/:organizationId/audits/:auditId" element={<AuditDetailsPage />} />
            </Routes>
        </>
    );
}