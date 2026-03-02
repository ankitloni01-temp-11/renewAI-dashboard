import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useHumanQueue } from '../hooks/useHumanQueue'
import { Clock, AlertTriangle, User, ChevronRight, RefreshCw } from 'lucide-react'
import { QueueCase } from '../types'
import { timeAgo, formatDateShort } from '../utils/formatDate'
import { formatINR } from '../utils/formatCurrency'
import api from '../api/client'
import toast from 'react-hot-toast'
import { useAuthStore } from '../stores/authStore'
import { useQueryClient } from '@tanstack/react-query'

const REASON_LABELS: Record<string, string> = {
  distress_bereavement: '💔 Bereavement', distress_financial_hardship: '💰 Hardship',
  distress_medical: '🏥 Medical', human_requested: '🙋 Human Requested',
  critique_failure: '🤖 AI Critique Failed', compliance_flag: '⚖️ Compliance Flag',
}

function SLATimer({ escalatedAt, slaHours }: { escalatedAt: string; slaHours: number }) {
  const elapsed = (Date.now() - new Date(escalatedAt).getTime()) / 3600000
  const remaining = slaHours - elapsed
  const isOverdue = remaining <= 0
  const pct = Math.min(100, (elapsed / slaHours) * 100)
  const hh = Math.max(0, Math.floor(remaining))
  const mm = Math.max(0, Math.floor((remaining - hh) * 60))

  return (
    <div className="space-y-1">
      <div className={`text-xs font-medium ${isOverdue ? 'text-red-600' : remaining < 0.5 ? 'text-yellow-600' : 'text-green-600'}`}>
        {isOverdue ? '⚠️ OVERDUE' : `⏱ ${hh}h ${mm}m left`}
      </div>
      <div className="w-full bg-gray-100 rounded-full h-1">
        <div className={`h-1 rounded-full ${isOverdue ? 'bg-red-500' : remaining < 0.5 ? 'bg-yellow-400' : 'bg-green-400'}`}
          style={{ width: `${pct}%` }} />
      </div>
    </div>
  )
}

export default function CaseQueuePage() {
  const { data, isLoading, refetch } = useHumanQueue()
  const [filter, setFilter] = useState('all')
  const { user } = useAuthStore()
  const navigate = useNavigate()
  const qc = useQueryClient()

  const cases: QueueCase[] = data?.cases || []
  const filtered = filter === 'all' ? cases : cases.filter(c => {
    if (filter === 'distress') return c.reason.includes('distress')
    if (filter === 'critique') return c.reason === 'critique_failure'
    if (filter === 'human') return c.reason === 'human_requested'
    if (filter === 'compliance') return c.reason === 'compliance_flag'
    if (filter === 'urgent') return c.priority === 'URGENT'
    return true
  })

  const urgentCount = cases.filter(c => c.priority === 'URGENT' && c.status === 'unassigned').length

  const pickUp = async (caseId: string, e: React.MouseEvent) => {
    e.stopPropagation()
    try {
      await api.put(`/api/human-queue/${caseId}/assign?assigned_to=${user?.id || 'EMP-001'}`)
      toast.success('Case picked up!')
      qc.invalidateQueries({ queryKey: ['queue'] })
    } catch { toast.error('Failed to assign') }
  }

  if (isLoading) return <div className="flex items-center justify-center h-64 text-gray-500">Loading queue...</div>

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Case Queue</h1>
          <p className="text-sm text-gray-500">{cases.length} total cases • {urgentCount} urgent unassigned</p>
        </div>
        <button onClick={() => refetch()} className="flex items-center gap-1 text-sm text-blue-600 hover:text-blue-800">
          <RefreshCw className="w-4 h-4" /> Refresh
        </button>
      </div>

      {/* Filters */}
      <div className="flex gap-2 flex-wrap">
        {[['all','All Cases'],['urgent','🚨 Urgent'],['distress','💔 Distress'],['critique','🤖 AI Failed'],['human','🙋 Human Req'],['compliance','⚖️ Compliance']].map(([v,l]) => (
          <button key={v} onClick={() => setFilter(v)}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${filter===v ? 'bg-[#1B4F8A] text-white' : 'bg-white text-gray-600 border hover:border-blue-300'}`}>
            {l} {v === 'all' ? `(${cases.length})` : `(${cases.filter(c => v==='urgent' ? c.priority==='URGENT' : v==='distress' ? c.reason.includes('distress') : c.reason.includes(v)).length})`}
          </button>
        ))}
      </div>

      {/* Cases */}
      <div className="space-y-3">
        {filtered.length === 0 && <div className="bg-white rounded-xl p-8 text-center text-gray-500">No cases in this category</div>}
        {filtered.map(c => (
          <div key={c.case_id} onClick={() => navigate(`/queue/${c.case_id}`)}
            className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 hover:border-blue-300 hover:shadow-md transition-all cursor-pointer">
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${c.priority==='URGENT' ? 'bg-red-100 text-red-700' : 'bg-yellow-100 text-yellow-700'}`}>
                    {c.priority}
                  </span>
                  <span className="text-sm font-semibold text-gray-900">{c.customer_name}</span>
                  <span className="text-xs text-gray-400">{c.policy_id}</span>
                </div>
                <div className="text-xs text-gray-600 mb-2">{REASON_LABELS[c.reason] || c.reason}</div>
                <p className="text-sm text-gray-700 line-clamp-2 mb-2">{c.escalation_summary}</p>
                <div className="flex items-center gap-4 text-xs text-gray-500">
                  <span>📋 {c.policy_id}</span>
                  {c.premium_amount && <span>💰 {formatINR(c.premium_amount)}</span>}
                  <span className={`font-medium ${c.risk_level==='HIGH' ? 'text-red-600' : c.risk_level==='MEDIUM' ? 'text-yellow-600' : 'text-green-600'}`}>{c.risk_level} RISK</span>
                  <span>🌐 {c.preferred_language}</span>
                  <span>📡 {c.channel_detected}</span>
                </div>
              </div>
              <div className="flex flex-col items-end gap-2 min-w-32">
                <SLATimer escalatedAt={c.escalated_at} slaHours={c.sla_hours} />
                <div className="text-xs text-gray-400">{timeAgo(c.escalated_at)}</div>
                <div className="flex items-center gap-2">
                  {c.status === 'unassigned'
                    ? <button onClick={(e) => pickUp(c.case_id, e)} className="text-xs bg-[#1B4F8A] text-white px-3 py-1 rounded-lg hover:bg-blue-800">PICK UP</button>
                    : <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-lg">{c.status}</span>
                  }
                  <ChevronRight className="w-4 h-4 text-gray-400" />
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
