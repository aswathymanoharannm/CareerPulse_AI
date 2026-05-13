import { Routes, Route } from 'react-router-dom'
import LandingPage from './pages/LandingPage'
import LoginPage from './pages/LoginPage'
import AdminDashboard from './pages/AdminDashboard'
import HRDashboard from './pages/HRDashboard'
import StudentDashboard from './pages/StudentDashboard'
import Navbar from './components/Navbar'

function App() {
  return (
    <div className="min-h-screen bg-dark text-light">
      <Navbar />
      <main className="container mx-auto px-4 py-8">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/hr" element={<HRDashboard />} />
          <Route path="/student" element={<StudentDashboard />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
