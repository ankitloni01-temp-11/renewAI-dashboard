import { NavLink, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../stores/authStore'
import { 
  LayoutDashboard, Users, GitBranch, Bot, Search, 
  AlertTriangle, LogOut, Shield, TrendingUp, Activity
} from 'lucide-react'

const navItems = [
  { path: '/kpis', icon: LayoutDashboard, label: 'Executive KPIs', roles: ['renewal_head', 'admin'] },
  { path: '/queue', icon: Users, label: 'Case Queue', roles: ['senior_rrm', 'revival_specialist', 'compliance_handler', 'renewal_head', 'admin'] },
  { path: '/journeys', icon: GitBranch, label: 'Journeys', roles: ['admin', 'renewal_head', 'ai_ops_manager'] },
  { path: '/ai-ops', icon: Bot, label: 'AI Operations', roles: ['ai_ops_manager', 'admin'] },
  { path: '/trace', icon: Search, label: 'Trace Investigation', roles: ['compliance_handler', 'admin', 'renewal_head'] },
  { path: '/grievance', icon: AlertTriangle, label: 'Grievance Register', roles: ['compliance_handler', 'admin'] },
]

export default function Sidebar() {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()

  const visibleItems = navItems.filter(item => 
    !item.roles || item.roles.includes(user?.role || '')
  )

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

      {/* Nav */}
      <nav className="flex-1 px-2 py-4 space-y-1 overflow-y-auto">
        {visibleItems.map(item => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all ${
                isActive
                  ? 'bg-white text-[#1B4F8A] font-semibold shadow'
                  : 'text-blue-100 hover:bg-blue-700'
              }`
            }
          >
            <item.icon className="w-4 h-4 flex-shrink-0" />
            {item.label}
          </NavLink>
        ))}
      </nav>

      {/* Stats */}
      <div className="px-4 py-3 border-t border-blue-700 space-y-1">
        <div className="flex justify-between text-xs text-blue-300">
          <span>Policyholders</span>
          <span className="text-white font-medium">4.8M</span>
        </div>
        <div className="flex justify-between text-xs text-blue-300">
          <span>Renewals/day</span>
          <span className="text-white font-medium">~3,900</span>
        </div>
        <div className="flex justify-between text-xs text-blue-300">
          <span>Team Size</span>
          <span className="text-yellow-300 font-medium">20 specialists</span>
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
