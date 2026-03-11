import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './stores/authStore'
import LoginPage from './pages/LoginPage'
import Layout from './components/Layout'
import ExecutiveKPIPage from './pages/ExecutiveKPIPage'
import CaseQueuePage from './pages/CaseQueuePage'
import CaseDetailPage from './pages/CaseDetailPage'
import AIOpsPage from './pages/AIOpsPage'
import TraceInvestigationPage from './pages/TraceInvestigationPage'
import GrievancePage from './pages/GrievancePage'
import JourneysPage from './pages/JourneysPage'
import RevivalPage from './pages/RevivalPage'
import PoliciesPage from './pages/PoliciesPage'
import EscalationPage from './pages/EscalationPage'
import AuditLogPage from './pages/AuditLogPage'
import AgentsPage from './pages/AgentsPage'
import PromptsPage from './pages/PromptsPage'

function PlaceholderPage({ title }: { title: string }) {
  return <div className="p-8"><h1 className="text-2xl font-bold text-gray-700">{title}</h1><p className="text-gray-500 mt-2">Coming soon...</p></div>
}

function App() {
  const { user } = useAuthStore()

  if (!user) {
    return <LoginPage />
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/kpis" replace />} />
          <Route path="kpis" element={<ExecutiveKPIPage />} />
          <Route path="policies" element={<PoliciesPage />} />
          <Route path="journeys" element={<JourneysPage />} />
          <Route path="agents" element={<AgentsPage />} />
          <Route path="prompts" element={<PromptsPage />} />
          <Route path="trace" element={<TraceInvestigationPage />} />
          <Route path="escalation" element={<EscalationPage />} />
          <Route path="audit-log" element={<AuditLogPage />} />
          <Route path="queue" element={<CaseQueuePage />} />
          <Route path="queue/:caseId" element={<CaseDetailPage />} />
          <Route path="ai-ops" element={<AIOpsPage />} />
          <Route path="grievance" element={<GrievancePage />} />
          <Route path="revival" element={<RevivalPage />} />
          <Route path="*" element={<Navigate to="/kpis" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
