import { UserRole } from '../types'
export const ROLES: Array<{ id: UserRole; name: string; home: string }> = [
  { id: 'renewal_head', name: 'Ashwin Tiwari (Renewal Head)', home: '/kpis' },
  { id: 'senior_rrm', name: 'Priya Sharma (Senior RRM)', home: '/queue' },
  { id: 'revival_specialist', name: 'Rahul Deshmukh (Revival Specialist)', home: '/queue' },
  { id: 'compliance_handler', name: 'Ritu Agarwal (Compliance Handler)', home: '/trace' },
  { id: 'ai_ops_manager', name: 'Divya Menon (AI Ops Manager)', home: '/ai-ops' },
  { id: 'admin', name: 'Admin (See All)', home: '/kpis' }
]
export const canAccess = (role: UserRole, path: string): boolean => {
  const rules: Record<string, UserRole[]> = {
    '/kpis': ['renewal_head', 'admin'],
    '/queue': ['senior_rrm', 'revival_specialist', 'compliance_handler', 'renewal_head', 'admin'],
    '/trace': ['compliance_handler', 'admin', 'renewal_head'],
    '/ai-ops': ['ai_ops_manager', 'admin'],
    '/grievance': ['compliance_handler', 'admin'],
    '/journeys': ['admin', 'renewal_head', 'ai_ops_manager']
  }
  const allowed = rules[path]
  if (!allowed) return true
  return allowed.includes(role)
}
