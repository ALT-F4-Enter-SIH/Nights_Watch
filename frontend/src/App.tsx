import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/layout/Layout'
import Dashboard from './pages/Dashboard'
import InvestigationsPage from './pages/InvestigationsPage'
import GraphPage from './pages/GraphPage'
import CorrelationPage from './pages/CorrelationPage'
import StylometryPage from './pages/StylometryPage'
import BehaviorPage from './pages/BehaviorPage'
import InfrastructurePage from './pages/InfrastructurePage'
import EvidencePage from './pages/EvidencePage'
import ReportsPage from './pages/ReportsPage'
import SettingsPage from './pages/SettingsPage'
import ReplayPage from './pages/ReplayPage'

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/investigations" element={<InvestigationsPage />} />
          <Route path="/graph" element={<GraphPage />} />
          <Route path="/correlation" element={<CorrelationPage />} />
          <Route path="/stylometry" element={<StylometryPage />} />
          <Route path="/behavior" element={<BehaviorPage />} />
          <Route path="/infrastructure" element={<InfrastructurePage />} />
          <Route path="/evidence" element={<EvidencePage />} />
          <Route path="/reports" element={<ReportsPage />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route path="/replay" element={<ReplayPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}

export default App
