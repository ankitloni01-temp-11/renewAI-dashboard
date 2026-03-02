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

function App() {
  const { user } = useAuthStore()

  if (!user) {
    return <LoginPage />
  }

  const homeRoute = {
    renewal_head: '/kpis',
    senior_rrm: '/queue',
    revival_specialist: '/revival',
    compliance_handler: '/trace',
    ai_ops_manager: '/ai-ops',
    admin: '/kpis'
  }[user.role] || '/kpis'

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to={homeRoute} replace />} />
          <Route path="kpis" element={<ExecutiveKPIPage />} />
          <Route path="queue" element={<CaseQueuePage />} />
          <Route path="queue/:caseId" element={<CaseDetailPage />} />
          <Route path="ai-ops" element={<AIOpsPage />} />
          <Route path="trace" element={<TraceInvestigationPage />} />
          <Route path="grievance" element={<GrievancePage />} />
          <Route path="journeys" element={<JourneysPage />} />
          <Route path="revival" element={<RevivalPage />} />
          <Route path="*" element={<Navigate to={homeRoute} replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
