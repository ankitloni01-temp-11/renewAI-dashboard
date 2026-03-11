import { useParams, useNavigate } from 'react-router-dom'
import { useQueueCase } from '../hooks/useHumanQueue'
import { useAuditTrail } from '../hooks/useAuditTrail'
import { ArrowLeft, CheckCircle, Clock, MessageSquare, Mail, Phone } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { formatDate, timeAgo } from '../utils/formatDate'
import { formatINR } from '../utils/formatCurrency'
import api from '../api/client'
import toast from 'react-hot-toast'
import { useState } from 'react'
import { useAuthStore } from '../stores/authStore'
import { useQueryClient } from '@tanstack/react-query'

const CHANNEL_ICONS: Record<string, JSX.Element> = {
  whatsapp: <MessageSquare className="w-3 h-3 text-green-600" />,
  email: <Mail className="w-3 h-3 text-blue-600" />,
  voice: <Phone className="w-3 h-3 text-purple-600" />,
}

export default function CaseDetailPage() {
  const { caseId } = useParams<{ caseId: string }>()
  const navigate = useNavigate()
  const { data, isLoading } = useQueueCase(caseId || '')
  const { data: auditData } = useAuditTrail(data?.policy_id || '')
  const [resolution, setResolution] = useState('')
  const [notes, setNotes] = useState('')
  const [resolving, setResolving] = useState(false)
  const { user } = useAuthStore()
  const qc = useQueryClient()

  if (isLoading) return <div className="p-8 text-gray-500">Loading case...</div>
  if (!data || data.error) return <div className="p-8 text-red-500">Case not found</div>

  const c = data, policy = data.policy || {}, customer = data.customer || {}

  const resolveCase = async () => {
    if (!resolution) { toast.error('Select a resolution'); return }
    setResolving(true)
    try {
      await api.put(`/api/human-queue/${caseId}/resolve?resolution=${encodeURIComponent(resolution)}&notes=${encodeURIComponent(notes)}&resolved_by=${user?.id || 'EMP-001'}`)
      toast.success('Case resolved!')
      qc.invalidateQueries({ queryKey: ['queue'] })
      navigate('/queue')
    } catch { toast.error('Resolution failed') } finally { setResolving(false) }
  }

  const paymentDots = (policy.payment_history || []).map((ph: { status: string }) => ({
    color: ph.status === 'on_time' ? '#22c55e' : ph.status.includes('late') ? '#f59e0b' : '#ef4444'
  }))

  const conversations = data.conversation_history || []

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <button onClick={() => navigate('/queue')} className="flex items-center gap-1 text-sm text-blue-600 hover:text-blue-800">
          <ArrowLeft className="w-4 h-4" /> Back to Queue
        </button>
        <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${c.priority === 'URGENT' ? 'bg-red-100 text-red-700' : 'bg-yellow-100 text-yellow-700'}`}>{c.priority}</span>
        <h1 className="text-xl font-bold text-gray-900">{c.customer_name}</h1>
        <span className="text-sm text-gray-500">{c.policy_id}</span>
      </div>

      <div className="grid grid-cols-3 gap-4">
        {/* Policy Summary */}
        <div className="bg-white rounded-xl p-4 shadow-sm border">
          <h3 className="font-semibold text-gray-800 mb-3">Policy Summary</h3>
          <dl className="space-y-2 text-sm">
            <div className="flex justify-between"><dt className="text-gray-500">Product</dt><dd className="font-medium">{policy.product_name}</dd></div>
            <div className="flex justify-between"><dt className="text-gray-500">Premium</dt><dd className="font-bold text-blue-700">{formatINR(policy.premium_amount)}</dd></div>
            <div className="flex justify-between"><dt className="text-gray-500">Sum Assured</dt><dd className="font-medium">{formatINR(policy.sum_assured)}</dd></div>
            <div className="flex justify-between"><dt className="text-gray-500">Due Date</dt><dd className="font-medium">{policy.due_date}</dd></div>
            <div className="flex justify-between"><dt className="text-gray-500">Tenure</dt><dd>{customer.tenure_years} years</dd></div>
            <div className="flex justify-between"><dt className="text-gray-500">Segment</dt><dd className="capitalize">{customer.segment?.replace(/_/g, ' ')}</dd></div>
            <div className="flex justify-between"><dt className="text-gray-500">Language</dt><dd>{customer.preferred_language}</dd></div>
          </dl>
          {paymentDots.length > 0 && (
            <div className="mt-3">
              <p className="text-xs text-gray-500 mb-1">Payment History</p>
              <div className="flex gap-1 flex-wrap">
                {paymentDots.map((d: { color: string }, i: number) => <div key={i} className="w-4 h-4 rounded-full" style={{ backgroundColor: d.color }} title={`Year ${i + 1}`} />)}
              </div>
            </div>
          )}
        </div>

        {/* Briefing Note */}
        <div className="col-span-2 bg-white rounded-xl p-4 shadow-sm border">
          <h3 className="font-semibold text-gray-800 mb-3">AI Briefing Note</h3>
          <div className="bg-blue-50 rounded-lg p-3 text-sm prose prose-sm max-w-none">
            {c.briefing_note
              ? <ReactMarkdown>{c.briefing_note}</ReactMarkdown>
              : <p className="text-gray-500 italic">Briefing note not available. Run the demo journey to generate one.</p>
            }
          </div>
          {c.recommended_resolution_options && c.recommended_resolution_options.length > 0 && (
            <div className="mt-3">
              <p className="text-xs font-semibold text-gray-600 mb-2">Recommended Actions:</p>
              <div className="flex flex-wrap gap-2">
                {c.recommended_resolution_options.map((opt: string) => (
                  <span key={opt} className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full border border-green-200">{opt}</span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Conversation Timeline */}
      <div className="bg-white rounded-xl p-4 shadow-sm border">
        <h3 className="font-semibold text-gray-800 mb-3">Conversation Timeline</h3>
        {conversations.length === 0
          ? <p className="text-sm text-gray-500 italic">No conversation history. Run Meenakshi's demo journey and type a distress message in WhatsApp Simulator.</p>
          : <div className="space-y-2">
            {conversations.slice(-10).map((msg: Record<string, string>, i: number) => (
              <div key={i} className={`flex gap-3 ${msg.role === 'ai' ? '' : 'flex-row-reverse'}`}>
                <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 ${msg.role === 'ai' ? 'bg-blue-600 text-white' : 'bg-green-600 text-white'}`}>
                  {msg.role === 'ai' ? 'AI' : 'C'}
                </div>
                <div className={`flex-1 max-w-lg rounded-lg p-2 text-sm ${msg.role === 'ai' ? 'bg-blue-50' : 'bg-green-50'}`}>
                  <p>{msg.ai_response || msg.customer_text}</p>
                  <div className="flex gap-2 mt-1">
                    {msg.detected_intent && <span className="text-xs text-gray-400">{msg.detected_intent}</span>}
                    {msg.critique_score && <span className="text-xs text-blue-600">{parseFloat(msg.critique_score).toFixed(1)}/10</span>}
                    <span className="text-xs text-gray-400">{formatDate(msg.timestamp)}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        }
      </div>

      {/* Audit Trail */}
      <div className="bg-white rounded-xl p-4 shadow-sm border">
        <h3 className="font-semibold text-gray-800 mb-3">Agent Audit Trail ({auditData?.total || 0} steps)</h3>
        <div className="space-y-2 max-h-48 overflow-y-auto">
          {(auditData?.entries || []).slice(-8).map((e: Record<string, string | number>, i: number) => (
            <div key={i} className="flex items-start gap-3 text-xs border-b border-gray-50 pb-2">
              <span className={`px-1.5 py-0.5 rounded font-bold ${e.verdict === 'APPROVED' || e.verdict === 'SENT' ? 'bg-green-100 text-green-700' : e.verdict === 'ESCALATED' ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'}`}>{String(e.verdict || 'OK')}</span>
              <div className="flex-1"><span className="font-medium text-blue-700">{String(e.agent_name)}</span> — {String(e.output_summary)}</div>
              {e.critique_score && <span className="text-blue-600">{Number(e.critique_score).toFixed(1)}/10</span>}
              <span className="text-gray-400">{e.latency_ms}ms</span>
            </div>
          ))}
        </div>
      </div>

      {/* Resolution Form */}
      <div className="bg-white rounded-xl p-4 shadow-sm border">
        <h3 className="font-semibold text-gray-800 mb-3">Resolve Case</h3>
        <div className="grid grid-cols-2 gap-3 mb-3">
          {['Policy renewed - payment collected', 'Premium holiday granted (3 months)', 'Death benefit claim initiated', 'Revival fee waived', 'Customer chose to lapse (informed decision)', 'Escalated further to senior specialist', 'Other'].map(opt => (
            <label key={opt} className={`flex items-center gap-2 p-2 rounded-lg border cursor-pointer text-sm transition-all ${resolution === opt ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'}`}>
              <input type="radio" name="resolution" value={opt} onChange={() => setResolution(opt)} className="text-blue-600" />
              {opt}
            </label>
          ))}
        </div>
        <textarea value={notes} onChange={e => setNotes(e.target.value)} rows={2}
          placeholder="Add resolution notes for audit trail..." className="w-full border rounded-lg p-2 text-sm resize-none focus:outline-none focus:border-blue-400" />
        <div className="flex gap-2 mt-3">
          <button onClick={resolveCase} disabled={resolving || !resolution}
            className="flex items-center gap-2 bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white px-4 py-2 rounded-lg text-sm font-medium transition-all">
            <CheckCircle className="w-4 h-4" /> {resolving ? 'Resolving...' : 'Resolve Case'}
          </button>
          <button onClick={() => navigate('/queue')} className="px-4 py-2 rounded-lg text-sm border border-gray-300 hover:bg-gray-50 transition-all">
            Back to Queue
          </button>
        </div>
      </div>
    </div>
  )
}
