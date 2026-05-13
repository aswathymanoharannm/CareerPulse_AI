import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Users, UserPlus, Trash2, ShieldCheck, Mail, Key } from 'lucide-react'

const AdminDashboard = () => {
  const [hrs, setHrs] = useState([])
  const [showAddModal, setShowAddModal] = useState(false)
  const [newHR, setNewHR] = useState({ name: '', email: '', password: '' })
  const [loading, setLoading] = useState(true)

  const token = localStorage.getItem('token')

  useEffect(() => {
    fetchHrs()
  }, [])

  const fetchHrs = async () => {
    try {
      const res = await fetch('/api/admin/hr', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      const data = await res.json()
      setHrs(Array.isArray(data) ? data : [])
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleAddHR = async (e) => {
    e.preventDefault()
    try {
      const res = await fetch('/api/admin/hr', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(newHR)
      })
      if (res.ok) {
        setShowAddModal(false)
        setNewHR({ name: '', email: '', password: '' })
        fetchHrs()
      }
    } catch (err) {
      console.error(err)
    }
  }

  const handleDeleteHR = async (id) => {
    if (!window.confirm('Are you sure you want to delete this HR?')) return
    try {
      const res = await fetch(`/api/admin/hr/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if (res.ok) fetchHrs()
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-4xl font-black mb-2">Admin Panel</h1>
          <p className="text-slate-400">Manage HR personnel and oversee platform activity.</p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="bg-primary hover:bg-primary/90 text-white px-6 py-3 rounded-2xl font-bold flex items-center gap-2 transition-all hover:scale-105"
        >
          <UserPlus size={20} />
          <span>Add HR Personnel</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 bg-white/5 border border-white/10 rounded-3xl">
          <div className="text-slate-400 text-sm font-bold uppercase tracking-wider mb-2">Total HRs</div>
          <div className="text-4xl font-black">{hrs.length}</div>
        </div>
      </div>

      <div className="bg-white/5 border border-white/10 rounded-[32px] overflow-hidden">
        <table className="w-full text-left">
          <thead>
            <tr className="bg-white/5 border-b border-white/10">
              <th className="px-8 py-6 text-sm font-bold uppercase tracking-wider text-slate-400">Name</th>
              <th className="px-8 py-6 text-sm font-bold uppercase tracking-wider text-slate-400">Email</th>
              <th className="px-8 py-6 text-sm font-bold uppercase tracking-wider text-slate-400">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5">
            {hrs.map((hr) => (
              <tr key={hr.id} className="hover:bg-white/[0.02] transition-colors">
                <td className="px-8 py-6 font-bold">{hr.name}</td>
                <td className="px-8 py-6 text-slate-400">{hr.email}</td>
                <td className="px-8 py-6">
                  <button
                    onClick={() => handleDeleteHR(hr.id)}
                    className="p-3 bg-red-500/10 text-red-400 rounded-xl hover:bg-red-500/20 transition-colors"
                  >
                    <Trash2 size={18} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {hrs.length === 0 && !loading && (
          <div className="p-12 text-center text-slate-500">No HR personnel found. Add your first HR to get started.</div>
        )}
      </div>

      {/* Add Modal */}
      <AnimatePresence>
        {showAddModal && (
          <div className="fixed inset-0 z-[60] flex items-center justify-center p-4">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setShowAddModal(false)}
              className="absolute inset-0 bg-dark/80 backdrop-blur-sm"
            />
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              className="relative w-full max-w-md bg-slate-900 border border-white/10 rounded-[32px] p-8 shadow-2xl"
            >
              <h2 className="text-2xl font-black mb-6">Create HR Account</h2>
              <form onSubmit={handleAddHR} className="space-y-4">
                <div className="space-y-2">
                  <label className="text-xs font-bold text-slate-500 uppercase ml-1">Full Name</label>
                  <input
                    type="text"
                    required
                    value={newHR.name}
                    onChange={(e) => setNewHR({...newHR, name: e.target.value})}
                    className="w-full bg-white/5 border border-white/10 rounded-2xl p-4 outline-none focus:border-primary transition-all"
                    placeholder="Enter name"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-xs font-bold text-slate-500 uppercase ml-1">Email Address</label>
                  <input
                    type="email"
                    required
                    value={newHR.email}
                    onChange={(e) => setNewHR({...newHR, email: e.target.value})}
                    className="w-full bg-white/5 border border-white/10 rounded-2xl p-4 outline-none focus:border-primary transition-all"
                    placeholder="hr@institute.com"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-xs font-bold text-slate-500 uppercase ml-1">Temporary Password</label>
                  <input
                    type="password"
                    required
                    value={newHR.password}
                    onChange={(e) => setNewHR({...newHR, password: e.target.value})}
                    className="w-full bg-white/5 border border-white/10 rounded-2xl p-4 outline-none focus:border-primary transition-all"
                    placeholder="••••••••"
                  />
                </div>
                <div className="flex gap-4 pt-4">
                  <button
                    type="button"
                    onClick={() => setShowAddModal(false)}
                    className="flex-1 px-6 py-4 rounded-2xl font-bold bg-white/5 border border-white/10 hover:bg-white/10 transition-all"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="flex-1 px-6 py-4 rounded-2xl font-bold bg-primary hover:bg-primary/90 text-white transition-all shadow-lg shadow-primary/20"
                  >
                    Create Account
                  </button>
                </div>
              </form>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default AdminDashboard
