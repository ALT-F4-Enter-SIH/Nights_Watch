import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/layout/Layout'
import Dashboard from './pages/Dashboard'
import Identities from './pages/Identities'
import Relations from './pages/Relations'
import Analytics from './pages/Analytics'
import Import from './pages/Import'
import Settings from './pages/Settings'

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/identities" element={<Identities />} />
          <Route path="/relations" element={<Relations />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/import" element={<Import />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}

export default App
