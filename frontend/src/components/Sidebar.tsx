import { NavLink, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../stores/authStore'
import { useEffect, useState } from 'react'
import api from '../api/client'
import {
  LayoutDashboard, FileText, Bot,
  AlertTriangle, ClipboardList, GitBranch, Search,
  LogOut, Shield, Activity
} from 'lucide-react'

const sections = [
  {
    title: 'OPERATIONS',
    items: [
      { path: '/kpis', icon: LayoutDashboard, label: 'Overview' },
      { path: '/policies', icon: FileText, label: 'Policies' },
      { path: '/journeys', icon: GitBranch, label: 'Journeys' },
      { path: '/agents', icon: Bot, label: 'Agents' },
      { path: '/prompts', icon: FileText, label: 'Prompts' },
    ]
  },
  {
    title: 'INTELLIGENCE',
    items: [
      { path: '/trace', icon: Search, label: 'Trace Investigation' },
    ]
  },
  {
    title: 'HUMAN OVERSIGHT',
    items: [
      { path: '/escalation', icon: AlertTriangle, label: 'Escalation', badge: true },
      { path: '/audit-log', icon: ClipboardList, label: 'Audit Log' },
    ]
  },
]

export default function Sidebar() {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()
  const [openCases, setOpenCases] = useState(0)

  useEffect(() => {
    const fetchCases = () => {
      api.get('/api/human-queue?status=open').then(r => setOpenCases(r.data?.length || 0)).catch(() => { })
    }
    fetchCases()
    const iv = setInterval(fetchCases, 10000)
    return () => clearInterval(iv)
  }, [])

  return (
    <div className="w-64 bg-[#1B4F8A] text-white flex flex-col h-full shadow-xl">
      {/* Logo */}
      <div className="p-4 border-b border-blue-700">
        <div className="flex items-center gap-2 mb-1">
          <Shield className="w-7 h-7 text-yellow-400" />
          <div>
            <div className="font-bold text-lg leading-tight">RenewAI</div>
            <div className="text-xs text-blue-300">Suraksha Life Insurance</div>
          </div>
        </div>
      </div>

      {/* User */}
      <div className="px-4 py-3 border-b border-blue-700 bg-blue-900/30">
        <div className="text-xs text-blue-300">Logged in as</div>
        <div className="font-semibold text-sm truncate">{user?.name}</div>
        <div className="text-xs text-yellow-300 capitalize">{user?.role?.replace(/_/g, ' ')}</div>
      </div>

      {/* Nav Sections */}
      <nav className="flex-1 px-2 py-3 overflow-y-auto space-y-4">
        {sections.map(section => (
          <div key={section.title}>
            <div className="px-3 mb-1.5 text-[10px] font-bold text-blue-400 tracking-wider uppercase">{section.title}</div>
            <div className="space-y-0.5">
              {section.items.map(item => (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) =>
                    `flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-all ${isActive
                      ? 'bg-white text-[#1B4F8A] font-semibold shadow'
                      : 'text-blue-100 hover:bg-blue-700'
                    }`
                  }
                >
                  <item.icon className="w-4 h-4 flex-shrink-0" />
                  <span className="flex-1">{item.label}</span>
                  {item.badge && openCases > 0 && (
                    <span className="bg-red-500 text-white text-[10px] font-bold rounded-full w-5 h-5 flex items-center justify-center">{openCases}</span>
                  )}
                </NavLink>
              ))}
            </div>
          </div>
        ))}
      </nav>

      {/* AI Engine Status */}
      <div className="px-4 py-3 border-t border-blue-700">
        <div className="flex items-center gap-2 text-xs">
          <Activity className="w-3.5 h-3.5 text-green-400 animate-pulse" />
          <span className="text-green-400 font-medium">AI Engine Active</span>
        </div>
      </div>

      {/* Logout */}
      <button
        onClick={() => { logout(); navigate('/') }}
        className="flex items-center gap-2 px-4 py-3 text-sm text-blue-300 hover:text-white hover:bg-blue-700 transition-all border-t border-blue-700"
      >
        <LogOut className="w-4 h-4" />
        Switch Role
      </button>
    </div>
  )
}
