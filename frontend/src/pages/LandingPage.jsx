import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { CheckCircle, Zap, Shield, BarChart3, Users, Briefcase } from 'lucide-react'

const LandingPage = () => {
  return (
    <div className="space-y-24">
      {/* Hero Section */}
      <section className="relative pt-12 pb-24 overflow-hidden">
        <div className="absolute top-0 right-0 -z-10 w-[500px] h-[500px] bg-primary/20 blur-[120px] rounded-full" />
        <div className="absolute bottom-0 left-0 -z-10 w-[500px] h-[500px] bg-secondary/20 blur-[120px] rounded-full" />
        
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center space-y-8"
        >
          <h1 className="text-6xl md:text-8xl font-black tracking-tight leading-tight">
            Elevate Your <br />
            <span className="bg-gradient-to-r from-primary via-white to-secondary bg-clip-text text-transparent">
              Career Placement
            </span>
          </h1>
          <p className="text-xl text-slate-400 max-w-2xl mx-auto font-medium">
            Automate job discovery, personalized alerts, and student management 
            with our AI-powered placement platform.
          </p>
          <div className="flex justify-center gap-4 pt-4">
            <Link 
              to="/login" 
              className="bg-primary hover:bg-primary/90 text-white px-8 py-4 rounded-2xl text-lg font-bold shadow-lg shadow-primary/20 transition-all hover:-translate-y-1"
            >
              Get Started Now
            </Link>
            <button className="bg-white/5 hover:bg-white/10 border border-white/10 text-white px-8 py-4 rounded-2xl text-lg font-bold transition-all">
              View Demo
            </button>
          </div>
        </motion.div>
      </section>

      {/* Features Grid */}
      <section className="grid md:grid-cols-3 gap-8 px-4">
        {[
          { icon: <Zap className="text-yellow-400" />, title: "AI Job Scraping", desc: "Automated collection of AI and Data Science roles from top job portals." },
          { icon: <BarChart3 className="text-green-400" />, title: "Placement Analytics", desc: "Track student performance and application trends with visual dashboards." },
          { icon: <Shield className="text-blue-400" />, title: "Secure Automation", desc: "Enterprise-grade security with daily automated email alerts and reports." }
        ].map((feat, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.2 }}
            className="p-8 bg-white/5 border border-white/10 rounded-3xl hover:bg-white/10 transition-colors group"
          >
            <div className="w-12 h-12 bg-white/5 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              {feat.icon}
            </div>
            <h3 className="text-2xl font-bold mb-4">{feat.title}</h3>
            <p className="text-slate-400 leading-relaxed">{feat.desc}</p>
          </motion.div>
        ))}
      </section>

      {/* Stats Section */}
      <section className="bg-white/5 border border-white/10 rounded-[40px] p-12 md:p-24 relative overflow-hidden">
        <div className="grid md:grid-cols-4 gap-12 text-center relative z-10">
          {[
            { label: "Jobs Scraped", val: "10K+", icon: <Briefcase /> },
            { label: "Students Placed", val: "500+", icon: <Users /> },
            { label: "Success Rate", val: "94%", icon: <CheckCircle /> },
            { label: "Daily Alerts", val: "1.2K", icon: <Zap /> }
          ].map((stat, i) => (
            <div key={i} className="space-y-4">
              <div className="text-slate-500 flex justify-center mb-2">{stat.icon}</div>
              <div className="text-5xl font-black bg-gradient-to-b from-white to-white/50 bg-clip-text text-transparent">
                {stat.val}
              </div>
              <div className="text-sm font-bold tracking-widest text-primary uppercase">
                {stat.label}
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}

export default LandingPage
