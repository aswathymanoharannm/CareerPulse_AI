import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { GraduationCap, UserPlus, Trash2, Mail, Search, Github } from 'lucide-react'

const HRDashboard = () => {
  const [students, setStudents] = useState([])
  const [showAddModal, setShowAddModal] = useState(false)
  const [newStudent, setNewStudent] = useState({ name: '', email: '', skills: [], github_url: '' })
  const [skillInput, setSkillInput] = useState('')
  const [loading, setLoading] = useState(true)

  const token = localStorage.getItem('token')

  useEffect(() => {
    fetchStudents()
  }, [])

  const fetchStudents = async () => {
    try {
      const res = await fetch('/api/hr/students', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      const data = await res.json()
      setStudents(Array.isArray(data) ? data : [])
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleAddStudent = async (e) => {
    e.preventDefault()
    try {
      const res = await fetch('/api/hr/students', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(newStudent)
      })
      if (res.ok) {
        setShowAddModal(false)
        setNewStudent({ name: '', email: '', skills: [], github_url: '' })
        fetchStudents()
      }
    } catch (err) {
      console.error(err)
    }
  }

  const handleDeleteStudent = async (id) => {
    if (!window.confirm('Delete this student record?')) return
    try {
      const res = await fetch(`/api/hr/students/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if (res.ok) fetchStudents()
    } catch (err) {
      console.error(err)
    }
  }

  const addSkill = () => {
    if (skillInput && !newStudent.skills.includes(skillInput)) {
      setNewStudent({...newStudent, skills: [...newStudent.skills, skillInput]})
      setSkillInput('')
    }
  }

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-4xl font-black mb-2">Student Database</h1>
          <p className="text-slate-400">Add students to enroll them in daily AI/Data job alerts.</p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="bg-secondary hover:bg-secondary/90 text-white px-6 py-3 rounded-2xl font-bold flex items-center gap-2 transition-all hover:scale-105"
        >
          <UserPlus size={20} />
          <span>Add New Student</span>
        </button>
      </div>

      <div className="bg-white/5 border border-white/10 rounded-[32px] overflow-hidden">
        <table className="w-full text-left">
          <thead>
            <tr className="bg-white/5 border-b border-white/10">
              <th className="px-8 py-6 text-sm font-bold uppercase tracking-wider text-slate-400">Student Name</th>
              <th className="px-8 py-6 text-sm font-bold uppercase tracking-wider text-slate-400">Email Address</th>
              <th className="px-8 py-6 text-sm font-bold uppercase tracking-wider text-slate-400">Skills</th>
              <th className="px-8 py-6 text-sm font-bold uppercase tracking-wider text-slate-400">Profiles</th>
              <th className="px-8 py-6 text-sm font-bold uppercase tracking-wider text-slate-400">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5">
            {students.map((student) => (
              <tr key={student.id} className="hover:bg-white/[0.02] transition-colors">
                <td className="px-8 py-6">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-secondary/10 rounded-full flex items-center justify-center text-secondary">
                      <GraduationCap size={20} />
                    </div>
                    <span className="font-bold">{student.name}</span>
                  </div>
                </td>
                <td className="px-8 py-6 text-slate-400 font-medium">{student.email}</td>
                <td className="px-8 py-6">
                  <div className="flex flex-wrap gap-2">
                    {student.skills?.map((s, i) => (
                      <span key={i} className="px-3 py-1 bg-white/5 rounded-full text-xs font-bold border border-white/5">
                        {s}
                      </span>
                    )) || <span className="text-slate-600 text-xs italic">No skills listed</span>}
                  </div>
                </td>
                <td className="px-8 py-6">
                  {student.github_url && (
                    <a 
                      href={student.github_url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-2 px-3 py-1.5 bg-white/5 hover:bg-white/10 border border-white/5 rounded-xl text-xs font-bold text-slate-300 transition-all"
                    >
                      <Github size={14} />
                      GitHub
                    </a>
                  )}
                </td>
                <td className="px-8 py-6">
                  <button
                    onClick={() => handleDeleteStudent(student.id)}
                    className="p-3 bg-red-500/10 text-red-400 rounded-xl hover:bg-red-500/20 transition-colors"
                  >
                    <Trash2 size={18} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {students.length === 0 && !loading && (
          <div className="p-12 text-center text-slate-500">No students enrolled yet.</div>
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
              className="relative w-full max-w-lg bg-slate-900 border border-white/10 rounded-[32px] p-8 shadow-2xl"
            >
              <h2 className="text-2xl font-black mb-6">Enroll New Student</h2>
              <form onSubmit={handleAddStudent} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-xs font-bold text-slate-500 uppercase ml-1">Full Name</label>
                    <input
                      type="text"
                      required
                      value={newStudent.name}
                      onChange={(e) => setNewStudent({...newStudent, name: e.target.value})}
                      className="w-full bg-white/5 border border-white/10 rounded-2xl p-4 outline-none focus:border-secondary transition-all"
                      placeholder="John Doe"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-xs font-bold text-slate-500 uppercase ml-1">Email</label>
                    <input
                      type="email"
                      required
                      value={newStudent.email}
                      onChange={(e) => setNewStudent({...newStudent, email: e.target.value})}
                      className="w-full bg-white/5 border border-white/10 rounded-2xl p-4 outline-none focus:border-secondary transition-all"
                      placeholder="john@example.com"
                    />
                  </div>
                  </div>
                </div>

                <div className="space-y-2">
                  <label className="text-xs font-bold text-slate-500 uppercase ml-1">GitHub Profile URL (Optional)</label>
                  <div className="relative">
                    <Github className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
                    <input
                      type="url"
                      value={newStudent.github_url}
                      onChange={(e) => setNewStudent({...newStudent, github_url: e.target.value})}
                      className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-4 outline-none focus:border-secondary transition-all"
                      placeholder="https://github.com/username"
                    />
                  </div>
                </div>
                
                <div className="space-y-2">
                  <label className="text-xs font-bold text-slate-500 uppercase ml-1">Skills (Keywords for Job Matching)</label>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={skillInput}
                      onChange={(e) => setSkillInput(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addSkill())}
                      className="flex-1 bg-white/5 border border-white/10 rounded-2xl p-4 outline-none focus:border-secondary transition-all"
                      placeholder="e.g. Python, React, NLP"
                    />
                    <button
                      type="button"
                      onClick={addSkill}
                      className="px-6 bg-white/10 hover:bg-white/20 rounded-2xl font-bold transition-all"
                    >
                      Add
                    </button>
                  </div>
                  <div className="flex flex-wrap gap-2 pt-2">
                    {newStudent.skills.map((s, i) => (
                      <span key={i} className="px-3 py-1 bg-secondary/20 text-secondary border border-secondary/20 rounded-full text-xs font-bold flex items-center gap-2">
                        {s}
                        <button type="button" onClick={() => setNewStudent({...newStudent, skills: newStudent.skills.filter((_, idx) => idx !== i)})}>
                          ×
                        </button>
                      </span>
                    ))}
                  </div>
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
                    className="flex-1 px-6 py-4 rounded-2xl font-bold bg-secondary hover:bg-secondary/90 text-white transition-all shadow-lg shadow-secondary/20"
                  >
                    Enroll Student
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

export default HRDashboard
