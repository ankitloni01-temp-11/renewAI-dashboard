import { useState, useEffect } from 'react'
import { GitBranch, X, MessageSquare, Mail, Phone, Loader2 } from 'lucide-react'
import api from '../api/client'
import { useJourneys } from '../hooks/useJourneys'

const statusColors: Record<string, string> = {
  paid: 'bg-green-100 text-green-700', whatsapp_sent: 'bg-blue-100 text-blue-700',
  email_sent: 'bg-orange-100 text-orange-700', voice_called: 'bg-purple-100 text-purple-700',
  escalated: 'bg-red-100 text-red-700', lapsed: 'bg-gray-100 text-gray-500',
  started: 'bg-yellow-100 text-yellow-700',
}
const channelIcons: Record<string, any> = { whatsapp: MessageSquare, email: Mail, voice: Phone }
const LANG: Record<string, string> = { hi: 'Hindi', en: 'English', ta: 'Tamil', ur: 'Urdu', mr: 'Marathi' }
const fmt = (n: number) => '₹' + n.toLocaleString('en-IN')
const agentColor = (name: string) => {
  const n = name.toLowerCase()
  if (n.includes('orchestrator')) return '#2dd4a8'; if (n.includes('planner')) return '#f59e0b'
  if (n.includes('critique')) return '#f59e0b'; if (n.includes('safety')) return '#22c55e'
  return '#2dd4a8'
}
const relTime = (d: string) => {
  if (!d) return '-'
  const diff = Date.now() - new Date(d).getTime(); const h = Math.floor(diff / 3600000)
  if (h < 1) return 'just now'; if (h < 24) return `${h}h ago`; return `${Math.floor(h / 24)}d ago`
}

const TABS = ['all', 'paid', 'whatsapp_sent', 'email_sent', 'voice_called', 'escalated', 'lapsed', 'started']

export default function JourneysPage() {
  const [tab, setTab] = useState('all')
  const { data: journeys = [], isLoading } = useJourneys(tab === 'all' ? undefined : tab)
  const [detail, setDetail] = useState<any | null>(null)
  const [detailData, setDetailData] = useState<any | null>(null)

  const openDetail = (j: any) => {
    setDetail(j)
    api.get(`/api/journeys/${j.policy_id}`).then(r => setDetailData(r.data)).catch(() => { })
  }

  return (
    <div className="p-6">
      <div className="flex items-center gap-2 mb-4">
        <GitBranch className="w-5 h-5 text-teal-600" />
        <h1 className="text-xl font-bold text-gray-800">Journeys</h1>
      </div>

      {/* Filter tabs */}
      <div className="flex gap-1 mb-4 overflow-x-auto pb-1">
        {TABS.map(t => (
          <button key={t} onClick={() => setTab(t)}
            className={`px-3 py-1.5 text-xs rounded-full font-medium transition-colors whitespace-nowrap ${tab === t ? 'bg-teal-600 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}>
            {t === 'all' ? 'All' : t.replace(/_/g, ' ')}
          </button>
        ))}
      </div>

      <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b">
            <tr>{['Policy ID', 'Customer', 'Status', 'Step', 'Channel', 'Language', 'Premium', 'Due Date', 'Started', 'Updated', 'Payment'].map(h =>
              <th key={h} className="px-3 py-3 text-left text-[10px] font-semibold text-gray-500 uppercase">{h}</th>
            )}</tr>
          </thead>
          <tbody className="divide-y">
            {journeys.map((j: any) => {
              const ChIcon = channelIcons[j.channel] || MessageSquare
              return (
                <tr key={j.policy_id} onClick={() => openDetail(j)} className="hover:bg-blue-50 cursor-pointer transition-colors">
                  <td className="px-3 py-2.5 font-mono text-xs font-bold text-teal-700">{j.policy_id}</td>
                  <td className="px-3 py-2.5 font-medium text-gray-800">{j.customer_name}</td>
                  <td className="px-3 py-2.5"><span className={`text-[10px] px-2 py-0.5 rounded-full font-bold ${statusColors[j.status] || 'bg-gray-100'}`}>{j.status}</span></td>
                  <td className="px-3 py-2.5 text-xs text-gray-500 font-mono">{j.current_step}</td>
                  <td className="px-3 py-2.5"><ChIcon className="w-4 h-4 text-gray-500" /></td>
                  <td className="px-3 py-2.5 text-xs">{j.language_name || LANG[j.language] || j.language}</td>
                  <td className="px-3 py-2.5 font-medium">{j.premium ? fmt(j.premium) : '-'}</td>
                  <td className="px-3 py-2.5 text-xs text-gray-500">{j.due_date}</td>
                  <td className="px-3 py-2.5 text-xs text-gray-400">{relTime(j.started_at)}</td>
                  <td className="px-3 py-2.5 text-xs text-gray-400">{relTime(j.updated_at)}</td>
                  <td className="px-3 py-2.5 font-medium text-green-600">{j.payment_amount ? fmt(j.payment_amount) : '-'}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
        {journeys.length === 0 && <p className="text-center text-gray-400 py-12">No journeys found.</p>}
      </div>

      {/* Detail Panel */}
      {detail && detailData && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" onClick={() => { setDetail(null); setDetailData(null) }}>
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-3xl max-h-[85vh] overflow-hidden" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between px-6 py-4 border-b bg-gray-50">
              <h2 className="font-bold text-lg">{detailData.customer?.name} — {detailData.policy?.product_name}</h2>
              <button onClick={() => { setDetail(null); setDetailData(null) }} className="p-1 hover:bg-gray-200 rounded"><X className="w-5 h-5" /></button>
            </div>
            <div className="overflow-y-auto max-h-[75vh] p-6 space-y-6">
              {/* Customer Profile */}
              <section>
                <h3 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Customer Profile</h3>
                <div className="grid grid-cols-2 gap-3 text-sm">
                  <div><span className="text-gray-400">Name:</span> <strong>{detailData.customer?.name}</strong></div>
                  <div><span className="text-gray-400">Age:</span> {detailData.customer?.age}</div>
                  <div><span className="text-gray-400">City:</span> {detailData.customer?.city}</div>
                  <div><span className="text-gray-400">Phone:</span> {detailData.customer?.phone}</div>
                  <div><span className="text-gray-400">Email:</span> {detailData.customer?.email}</div>
                  <div><span className="text-gray-400">Segment:</span> {detailData.customer?.segment}</div>
                  <div><span className="text-gray-400">Language:</span> {LANG[detailData.customer?.preferred_language] || detailData.customer?.preferred_language}</div>
                </div>
              </section>

              {/* Policy Details */}
              <section>
                <h3 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Policy Details</h3>
                <div className="grid grid-cols-2 gap-3 text-sm">
                  <div><span className="text-gray-400">Policy:</span> <strong className="font-mono">{detailData.policy_id}</strong></div>
                  <div><span className="text-gray-400">Product:</span> {detailData.policy?.product_name}</div>
                  <div><span className="text-gray-400">Type:</span> {detailData.policy?.product_type}</div>
                  <div><span className="text-gray-400">Premium:</span> {fmt(detailData.policy?.premium || 0)}</div>
                  <div><span className="text-gray-400">Sum Assured:</span> {fmt(detailData.policy?.sum_assured || 0)}</div>
                  <div><span className="text-gray-400">Due Date:</span> {detailData.policy?.due_date}</div>
                </div>
              </section>

              {/* Journey Timeline */}
              <section>
                <h3 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">Agent Pipeline Timeline</h3>
                {detailData.audit_trail?.length === 0 && <p className="text-gray-400 text-sm">No audit data.</p>}
                <div className="space-y-3">
                  {detailData.audit_trail?.map((e: any, i: number) => (
                    <div key={i} className="flex gap-4 border-l-2 border-gray-200 pl-4">
                      <div className="text-xs text-gray-400 w-20 flex-shrink-0 font-mono pt-0.5">
                        {new Date(e.timestamp).toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                      </div>
                      <div className="flex-1">
                        <div className="font-bold text-xs" style={{ color: agentColor(e.agent_name) }}>{e.agent_name.toUpperCase()} • {e.action}</div>
                        <div className="text-xs text-gray-600 mt-0.5 whitespace-pre-wrap">{e.evidence}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </section>

              {/* Escalation Info */}
              {detailData.status === 'escalated' && (
                <section className="bg-red-50 rounded-lg p-4">
                  <h3 className="text-xs font-bold text-red-500 uppercase tracking-wider mb-2">⚠️ Escalated to Human Queue</h3>
                  <p className="text-sm text-gray-700">This journey was escalated due to detected distress or customer request. Check the Escalation page for case details.</p>
                </section>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
