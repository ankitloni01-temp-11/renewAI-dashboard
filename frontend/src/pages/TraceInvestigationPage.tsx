import { useState } from 'react'
import { Search, ChevronDown, ChevronRight } from 'lucide-react'
import { useAuditTrail } from '../hooks/useAuditTrail'
import api from '../api/client'

const DEMO_POLICIES = [
  { id: 'SLI-2298741', label: 'Rajesh Sharma - Term Shield' },
  { id: 'SLI-882341', label: 'Meenakshi Iyer - Endowment Plus' },
  { id: 'SLI-445678', label: 'Vikram Malhotra - ULIP' },
]

function AuditStep({ entry, index }: { entry: Record<string, unknown>; index: number }) {
  const [expanded, setExpanded] = useState(false)
  const verdict = String(entry.verdict || '')
  const color = ['APPROVED','SENT','COMPLETED','CREATED','SPOKEN'].includes(verdict)
    ? 'border-green-400 bg-green-50' : ['ESCALATED','REJECTED'].includes(verdict)
    ? 'border-red-400 bg-red-50' : 'border-blue-300 bg-blue-50'

  return (
    <div className={`border-l-4 ${color} rounded-r-lg p-3 mb-2`}>
      <div className="flex items-start justify-between cursor-pointer" onClick={() => setExpanded(!expanded)}>
        <div className="flex items-center gap-2 flex-1 min-w-0">
          <span className="text-xs font-bold text-gray-400 w-5">#{index+1}</span>
          <span className={`px-1.5 py-0.5 rounded text-xs font-bold ${['APPROVED','SENT','COMPLETED'].includes(verdict) ? 'bg-green-200 text-green-800' : ['ESCALATED','REJECTED'].includes(verdict) ? 'bg-red-200 text-red-800' : 'bg-blue-200 text-blue-800'}`}>{verdict || 'N/A'}</span>
          <span className="text-sm font-semibold text-blue-700">{String(entry.agent_name)}</span>
          <span className="text-xs text-gray-500 truncate">{String(entry.output_summary || '')}</span>
        </div>
        <div className="flex items-center gap-2 ml-2 flex-shrink-0">
          {entry.critique_score != null && <span className="text-xs bg-purple-100 text-purple-700 px-1.5 py-0.5 rounded font-medium">{Number(entry.critique_score).toFixed(1)}/10</span>}
          {entry.latency_ms != null && <span className="text-xs text-gray-400">{String(entry.latency_ms)}ms</span>}
          {expanded ? <ChevronDown className="w-4 h-4 text-gray-400" /> : <ChevronRight className="w-4 h-4 text-gray-400" />}
        </div>
      </div>
      {expanded && (
        <div className="mt-2 space-y-2">
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div><span className="text-gray-400">Input:</span> <span className="text-gray-700">{String(entry.input_summary || '')}</span></div>
            <div><span className="text-gray-400">Model:</span> <span className="text-gray-700">{String(entry.model_used || 'N/A')}</span></div>
            <div><span className="text-gray-400">Tokens In:</span> <span className="text-gray-700">{String(entry.token_count_in || 0)}</span></div>
            <div><span className="text-gray-400">Tokens Out:</span> <span className="text-gray-700">{String(entry.token_count_out || 0)}</span></div>
          </div>
          {entry.full_output && (
            <details className="mt-1">
              <summary className="text-xs text-blue-600 cursor-pointer hover:text-blue-800">View full JSON output</summary>
              <pre className="mt-1 text-xs bg-gray-900 text-green-400 p-2 rounded overflow-auto max-h-48 font-mono">
                {JSON.stringify(entry.full_output, null, 2)}
              </pre>
            </details>
          )}
        </div>
      )}
    </div>
  )
}

export default function TraceInvestigationPage() {
  const [selectedPolicy, setSelectedPolicy] = useState('SLI-2298741')
  const [customId, setCustomId] = useState('')
  const [searching, setSearching] = useState(false)
  const policyId = customId || selectedPolicy
  const { data: auditData, isLoading } = useAuditTrail(policyId)

  const entries = auditData?.entries || []

  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Trace Investigation</h1>
        <p className="text-sm text-gray-500 mt-1">Full agent-by-agent audit trail for any policy. IRDAI-ready.</p>
      </div>

      {/* Search */}
      <div className="bg-white rounded-xl p-4 shadow-sm border">
        <div className="flex gap-3">
          <div className="flex-1">
            <label className="text-xs text-gray-500 mb-1 block">Quick select demo policy</label>
            <select value={selectedPolicy} onChange={e => { setSelectedPolicy(e.target.value); setCustomId('') }}
              className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-400">
              {DEMO_POLICIES.map(p => <option key={p.id} value={p.id}>{p.label} ({p.id})</option>)}
            </select>
          </div>
          <div className="flex-1">
            <label className="text-xs text-gray-500 mb-1 block">Or enter any Policy ID</label>
            <div className="flex gap-2">
              <input value={customId} onChange={e => setCustomId(e.target.value)} placeholder="e.g. SLI-445678"
                className="flex-1 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-400" />
              <button className="bg-[#1B4F8A] text-white px-4 rounded-lg hover:bg-blue-800">
                <Search className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-3">
        {[
          { label: 'Total Steps', value: entries.length },
          { label: 'Approved', value: entries.filter((e: Record<string, unknown>) => ['APPROVED','SENT','COMPLETED'].includes(String(e.verdict||''))).length },
          { label: 'Escalated/Rejected', value: entries.filter((e: Record<string, unknown>) => ['ESCALATED','REJECTED'].includes(String(e.verdict||''))).length },
          { label: 'Avg Latency', value: entries.length ? Math.round(entries.reduce((s: number, e: Record<string, unknown>) => s + (Number(e.latency_ms)||0), 0) / entries.length) + 'ms' : '-' },
        ].map(s => (
          <div key={s.label} className="bg-white rounded-xl p-3 shadow-sm border text-center">
            <div className="text-2xl font-bold text-gray-900">{s.value}</div>
            <div className="text-xs text-gray-500">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Trace */}
      <div className="bg-white rounded-xl p-4 shadow-sm border">
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-semibold text-gray-800">Agent Trace — {policyId}</h3>
          <span className="text-xs text-gray-400">{entries.length} entries</span>
        </div>
        {isLoading && <div className="text-center py-8 text-gray-400">Loading trace...</div>}
        {!isLoading && entries.length === 0 && (
          <div className="text-center py-8 text-gray-400">
            <p>No audit trail found for <strong>{policyId}</strong></p>
            <p className="text-sm mt-1">Run a demo journey from the control panel to generate trace data.</p>
          </div>
        )}
        <div className="space-y-1 max-h-[60vh] overflow-y-auto">
          {entries.map((e: Record<string, unknown>, i: number) => <AuditStep key={i} entry={e} index={i} />)}
        </div>
      </div>
    </div>
  )
}
