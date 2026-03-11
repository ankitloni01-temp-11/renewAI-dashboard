import { useState, useEffect } from 'react'
import { Search, ChevronDown, ChevronRight, Activity } from 'lucide-react'
import { useAuditTrail } from '../hooks/useAuditTrail'

const DEMO_POLICIES = [
  { id: 'SLI-2298741', label: 'Rajesh Kumar - Term Shield Plus' },
  { id: 'SLI-8872134', label: 'Meenakshi Iyer - Endowment Plan' },
  { id: 'SLI-5567123', label: 'Vikram Mehta - Wealth Builder ULIP' },
  { id: 'SLI-7754321', label: 'Shanta Devi - Senior Care Plus' },
]

function AuditStep({ entry, index }: { entry: any; index: number }) {
  const [expanded, setExpanded] = useState(false)
  const isEscalated = entry.action === 'ESCALATED_TO_HUMAN' || entry.action === 'WHATSAPP_FAIL'
  const isApproved = entry.action.includes('PASSED') || entry.action.includes('SENT') || entry.action === 'PAYMENT_CONFIRMED'

  const color = isEscalated ? 'border-red-400 bg-red-50' : isApproved ? 'border-green-400 bg-green-50' : 'border-blue-300 bg-blue-50'
  const badgeColor = isEscalated ? 'bg-red-200 text-red-800' : isApproved ? 'bg-green-200 text-green-800' : 'bg-blue-200 text-blue-800'

  return (
    <div className={`border-l-4 ${color} rounded-r-lg p-3 mb-2 shadow-sm`}>
      <div className="flex items-start justify-between cursor-pointer" onClick={() => setExpanded(!expanded)}>
        <div className="flex items-center gap-3 flex-1 min-w-0">
          <span className="text-[10px] font-bold text-gray-400 w-5">#{index + 1}</span>
          <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${badgeColor}`}>{entry.action}</span>
          <span className="text-sm font-bold text-gray-800">{entry.agent_name}</span>
          <span className="text-xs text-gray-500 truncate italic">"{entry.evidence?.slice(0, 60)}..."</span>
        </div>
        <div className="flex items-center gap-3 ml-2 flex-shrink-0">
          <span className="text-[10px] text-gray-400 font-mono">
            {new Date(entry.timestamp).toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
          </span>
          {expanded ? <ChevronDown className="w-4 h-4 text-gray-400" /> : <ChevronRight className="w-4 h-4 text-gray-400" />}
        </div>
      </div>
      {expanded && (
        <div className="mt-3 bg-white/50 rounded-lg p-3 space-y-2 border">
          <div className="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">
            {entry.evidence}
          </div>
          <div className="flex gap-4 pt-2 border-t text-[10px]">
            <div><span className="text-gray-400 uppercase font-bold">Policy:</span> <span className="font-mono text-teal-700">{entry.policy_id}</span></div>
            <div><span className="text-gray-400 uppercase font-bold">Prompt:</span> <span>{entry.prompt_version}</span></div>
          </div>
        </div>
      )}
    </div>
  )
}

export default function TraceInvestigationPage() {
  const [selectedPolicy, setSelectedPolicy] = useState('SLI-2298741')
  const [customId, setCustomId] = useState('')
  const [searchQuery, setSearchQuery] = useState('SLI-2298741')
  const { data: entries, isLoading } = useAuditTrail(searchQuery)

  useEffect(() => {
    if (!customId) setSearchQuery(selectedPolicy)
  }, [selectedPolicy, customId])

  const doSearch = () => {
    setSearchQuery(customId || selectedPolicy)
  }

  return (
    <div className="space-y-5 p-2">
      <div className="flex items-center gap-3">
        <Activity className="w-6 h-6 text-teal-600" />
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Trace Investigation</h1>
          <p className="text-sm text-gray-500">Deep agent-by-agent audit trail for compliance and debugging.</p>
        </div>
      </div>

      <div className="bg-white rounded-xl p-5 shadow-sm border">
        <div className="flex gap-4 items-end">
          <div className="flex-1">
            <label className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1.5 block">Quick Select</label>
            <select value={selectedPolicy} onChange={e => { setSelectedPolicy(e.target.value); setCustomId('') }}
              className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal-400 bg-gray-50 transition-all">
              {DEMO_POLICIES.map(p => <option key={p.id} value={p.id}>{p.label} ({p.id})</option>)}
            </select>
          </div>
          <div className="flex-1">
            <label className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1.5 block">Manual Search</label>
            <div className="flex gap-2">
              <input value={customId} onChange={e => setCustomId(e.target.value)} placeholder="Enter Policy ID..."
                className="flex-1 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal-400" />
              <button
                onClick={doSearch}
                className="bg-[#1B4F8A] text-white px-5 rounded-lg hover:bg-blue-800 transition-all flex items-center gap-2 text-sm font-semibold shadow-md active:scale-95"
              >
                <Search className="w-4 h-4" /> Trace
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl p-6 shadow-sm border min-h-[400px]">
        <div className="flex items-center justify-between mb-6 border-b pb-4">
          <div>
            <h3 className="font-bold text-gray-800 text-lg">Agent Decision Chain — {searchQuery}</h3>
            <p className="text-xs text-gray-400 mt-0.5 uppercase tracking-widest">IRDAI Compliance Log</p>
          </div>
          <div className="bg-teal-50 text-teal-700 px-3 py-1 rounded-full text-xs font-bold ring-1 ring-teal-200">
            {entries?.length || 0} Steps Recorded
          </div>
        </div>

        {isLoading && (
          <div className="flex flex-col items-center justify-center py-20 text-gray-400 animate-pulse">
            <Activity className="w-10 h-10 mb-2 text-teal-200" />
            <p className="text-sm font-medium">Reconstructing decision chain from audit data...</p>
          </div>
        )}

        {!isLoading && (!entries || entries.length === 0) && (
          <div className="text-center py-20 text-gray-400 border-2 border-dashed rounded-2xl">
            <Search className="w-12 h-12 mb-3 mx-auto text-gray-200" />
            <p className="font-bold text-gray-500">No audit trail found for {searchQuery}</p>
            <p className="text-xs mt-1">Please ensure the policy has processed through the AI pipeline.</p>
          </div>
        )}

        <div className="space-y-2">
          {entries?.map((e: any, i: number) => <AuditStep key={i} entry={e} index={i} />)}
        </div>
      </div>
    </div>
  )
}
