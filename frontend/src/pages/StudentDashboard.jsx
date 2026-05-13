import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Search, MapPin, Briefcase, ExternalLink, Filter, Sparkles } from 'lucide-react'

const StudentDashboard = () => {
  const [jobs, setJobs] = useState([])
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchJobs()
  }, [])

  const fetchJobs = async (skill = '') => {
    try {
      const url = skill ? `/api/jobs/?skill=${skill}` : '/api/jobs/'
      const res = await fetch(url)
      const data = await res.json()
      setJobs(Array.isArray(data) ? data : [])
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (e) => {
    e.preventDefault()
    setLoading(true)
    fetchJobs(search)
  }

  return (
    <div className="space-y-12">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h1 className="text-4xl font-black mb-2 flex items-center gap-3">
            Opportunities
            <Sparkles className="text-yellow-400" />
          </h1>
          <p className="text-slate-400 font-medium">Discover the latest AI and Data Science roles curated for you.</p>
        </div>

        <form onSubmit={handleSearch} className="relative flex-1 max-w-md">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" size={20} />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-4 outline-none focus:border-primary transition-all"
            placeholder="Search skills (e.g. Python, NLP)..."
          />
        </form>
      </div>

      {loading ? (
        <div className="grid md:grid-cols-2 gap-6">
          {[1, 2, 3, 4].map(i => (
            <div key={i} className="h-64 bg-white/5 rounded-3xl animate-pulse" />
          ))}
        </div>
      ) : (
        <div className="grid md:grid-cols-2 gap-6">
            {jobs.map((job, i) => (
            <motion.div
              key={job.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className="group p-8 bg-white/5 border border-white/10 rounded-[40px] hover:bg-white/10 transition-all hover:border-primary/50 relative overflow-hidden"
            >
              <div className="absolute top-0 right-0 p-8">
                 <span className="text-xs font-black uppercase tracking-widest text-slate-500 bg-white/5 px-4 py-2 rounded-full border border-white/5 group-hover:border-primary/30 group-hover:text-primary transition-colors">
                   New
                 </span>
              </div>

              <div className="flex flex-col h-full">
                <div className="mb-6">
                  <h3 className="text-2xl font-black mb-2 group-hover:text-primary transition-colors leading-tight">
                    {job.title}
                  </h3>
                  <div className="flex items-center gap-4 text-slate-400 font-bold text-sm">
                    <span className="flex items-center gap-1.5">
                      <Briefcase size={16} />
                      {job.company}
                    </span>
                    <span className="flex items-center gap-1.5">
                      <MapPin size={16} />
                      {job.location}
                    </span>
                  </div>
                </div>

                <div className="flex flex-wrap gap-2 mb-8 flex-1">
                  {job.skills.map((skill, idx) => (
                    <span key={idx} className="px-4 py-1.5 bg-white/5 border border-white/5 rounded-2xl text-xs font-bold text-slate-300 uppercase tracking-wide">
                      {skill}
                    </span>
                  ))}
                </div>

                <a
                  href={job.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-full bg-white/5 border border-white/10 group-hover:bg-primary text-white py-4 rounded-2xl font-bold flex items-center justify-center gap-2 transition-all group-hover:scale-[1.02]"
                >
                  Apply Now
                  <ExternalLink size={18} />
                </a>
              </div>
            </motion.div>
          ))}
          {jobs.length === 0 && (
            <div className="col-span-full py-24 text-center">
              <p className="text-xl text-slate-500 font-bold">No matching jobs found. Try adjusting your search.</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default StudentDashboard
