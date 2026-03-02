import { useState } from 'react'
import { Bot, AlertCircle } from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import api from '../api/client'

export default function AIOpsPage() {
  const { data: auditAll } = useQuery({ queryKey: ['audit-all'], queryFn: async () => { const { data } = await api.get('/api/audit?limit=200'); return data } })
  const { data: objData } = useQuery({ queryKey: ['objections'], queryFn: async () => { const { data } = await api.get('/api/data/objections'); return data } })
  const { data: kpiData } = useQuery({ queryKey: ['kpis'], queryFn: async () => { const { data } = await api.get('/api/kpis'); return data } })
  const [objFilter, setObjFilter] = useState('')

  const entries = auditAll?.entries || []
  const critiques = entries.filter((e: Record<string, unknown>) => e.critique_score != null)
  const avgScore = critiques.length ? (critiques.reduce((s: number, e: Record<string, unknown>) => s + Number(e.critique_score||0), 0) / critiques.length).toFixed(1) : 'N/A'
  const rejections = critiques.filter((e: Record<string, unknown>) => String(e.verdict||'') === 'REJECTED')

  const objections = (objData?.objections || []).filter((o: Record<string, string>) => !objFilter || o.objection_text.toLowerCase().includes(objFilter.toLowerCase()) || o.category.toLowerCase().includes(objFilter.toLowerCase()))

  const agentStats = ['EmailAgent','WhatsAppAgent','VoiceAgent','PlannerAgent','OrchestratorAgent'].map(name => {
    const agentEntries = entries.filter((e: Record<string, unknown>) => String(e.agent_name||'').startsWith(name.replace('Agent','')))
    const scored = agentEntries.filter((e: Record<string, unknown>) => e.critique_score != null)
    return {
      name, count: agentEntries.length,
      avgScore: scored.length ? (scored.reduce((s: number, e: Record<string, unknown>) => s + Number(e.critique_score||0), 0) / scored.length).toFixed(1) : 'N/A',
      avgLatency: agentEntries.length ? Math.round(agentEntries.reduce((s: number, e: Record<string, unknown>) => s + (Number(e.latency_ms)||0), 0) / agentEntries.length) : 0
    }
  })

  return (
    <div className="space-y-6">
      <div><h1 className="text-2xl font-bold text-gray-900">AI Operations</h1><p className="text-sm text-gray-500">Monitor agent performance, critique queue, objection library</p></div>

      {/* Health Cards */}
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: 'Total Agent Actions', value: entries.length, color: 'text-blue-700', bg: 'bg-blue-50' },
          { label: 'Avg Critique Score', value: `${avgScore}/10`, color: 'text-green-700', bg: 'bg-green-50' },
          { label: 'Critique Rejections', value: rejections.length, color: 'text-yellow-700', bg: 'bg-yellow-50' },
          { label: 'AI Accuracy', value: `${kpiData?.ai_accuracy_score || 89.2}%`, color: 'text-purple-700', bg: 'bg-purple-50' },
        ].map(c => (
          <div key={c.label} className={`${c.bg} rounded-xl p-4 border`}>
            <div className={`text-2xl font-bold ${c.color}`}>{c.value}</div>
            <div className="text-xs text-gray-500 mt-1">{c.label}</div>
          </div>
        ))}
      </div>

      {/* Agent Performance */}
      <div className="bg-white rounded-xl p-4 shadow-sm border">
        <h3 className="font-semibold text-gray-800 mb-3">Agent Performance</h3>
        <table className="w-full text-sm">
          <thead><tr className="text-left border-b text-xs text-gray-500">{['Agent','Actions','Avg Score','Avg Latency','Status'].map(h => <th key={h} className="pb-2 pr-4">{h}</th>)}</tr></thead>
          <tbody>{agentStats.map(a => (
            <tr key={a.name} className="border-b border-gray-50 hover:bg-gray-50">
              <td className="py-2 font-medium text-blue-700">{a.name}</td>
              <td className="py-2">{a.count}</td>
              <td className="py-2"><span className={`px-2 py-0.5 rounded text-xs font-medium ${parseFloat(a.avgScore) >= 7 ? 'bg-green-100 text-green-700' : a.avgScore === 'N/A' ? 'bg-gray-100 text-gray-500' : 'bg-yellow-100 text-yellow-700'}`}>{a.avgScore}</span></td>
              <td className="py-2">{a.avgLatency}ms</td>
              <td className="py-2"><span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded">Active</span></td>
            </tr>
          ))}</tbody>
        </table>
      </div>

      {/* Critique Queue */}
      <div className="bg-white rounded-xl p-4 shadow-sm border">
        <h3 className="font-semibold text-gray-800 mb-3">Critique Review Queue ({rejections.length} rejections)</h3>
        {rejections.length === 0
          ? <div className="text-center py-6 text-gray-400"><Bot className="w-8 h-8 mx-auto mb-2 opacity-30" /><p>No rejections — AI is performing well!</p></div>
          : <div className="space-y-2">
              {rejections.slice(0,5).map((e: Record<string, unknown>, i: number) => (
                <div key={i} className="flex items-start gap-3 p-3 bg-yellow-50 border border-yellow-200 rounded-lg text-sm">
                  <AlertCircle className="w-4 h-4 text-yellow-600 flex-shrink-0 mt-0.5" />
                  <div className="flex-1">
                    <span className="font-medium text-yellow-800">{String(e.agent_name)}</span>
                    <span className="text-gray-500 ml-2">Policy: {String(e.policy_id)}</span>
                    <p className="text-gray-700 mt-1">{String(e.output_summary||'')}</p>
                  </div>
                  <span className="text-xs bg-red-100 text-red-700 px-2 py-0.5 rounded font-medium">{Number(e.critique_score||0).toFixed(1)}/10</span>
                </div>
              ))}
            </div>
        }
      </div>

      {/* Objection Library */}
      <div className="bg-white rounded-xl p-4 shadow-sm border">
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-semibold text-gray-800">Objection Library ({objData?.total || 0} pairs)</h3>
          <input value={objFilter} onChange={e => setObjFilter(e.target.value)} placeholder="Search objections..."
            className="text-sm border border-gray-200 rounded-lg px-3 py-1.5 focus:outline-none focus:border-blue-400 w-48" />
        </div>
        <div className="space-y-2 max-h-64 overflow-y-auto">
          {objections.slice(0,20).map((o: Record<string, string | number>, i: number) => (
            <div key={i} className="border border-gray-100 rounded-lg p-3 hover:bg-gray-50">
              <div className="flex items-start justify-between gap-2">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded">{String(o.category).replace(/_/g,' ')}</span>
                    <span className="text-xs text-gray-400">Score: {Number(o.effectiveness_score).toFixed(1)}/10 • Used: {String(o.times_used)}x</span>
                  </div>
                  <p className="text-sm font-medium text-gray-800 mb-1">{String(o.objection_text)}</p>
                  <p className="text-xs text-gray-500 line-clamp-2">{String(o.response_english).slice(0,120)}...</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
