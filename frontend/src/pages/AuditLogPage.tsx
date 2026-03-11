import { useState, useEffect } from 'react'
import { Search, Download, ClipboardList, Shield, Filter } from 'lucide-react'
import api from '../api/client'

const agentBadge: Record<string, string> = {
    'ORCHESTRATOR': 'bg-teal-100 text-teal-700 border-teal-200',
    'PLANNER': 'bg-amber-100 text-amber-700 border-amber-200',
    'DRAFT_AND_GREETING': 'bg-blue-100 text-blue-700 border-blue-200',
    'CRITIQUE_A': 'bg-indigo-100 text-indigo-700 border-indigo-200',
    'CRITIQUE_B': 'bg-purple-100 text-purple-700 border-purple-200',
    'CONTENT_SAFETY': 'bg-red-100 text-red-700 border-red-200',
    'CHANNEL_ROUTER': 'bg-emerald-100 text-emerald-700 border-emerald-200',
    'WhatsApp Agent': 'bg-orange-100 text-orange-700 border-orange-200',
    'Email Agent': 'bg-sky-100 text-sky-700 border-sky-200',
    'Voice Agent': 'bg-violet-100 text-violet-700 border-violet-200',
}

export default function AuditLogPage() {
    const [entries, setEntries] = useState<any[]>([])
    const [search, setSearch] = useState('')
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        setLoading(true)
        api.get('/api/audit', { params: search ? { policy_id: search } : {} })
            .then(r => setEntries(r.data))
            .catch(() => { })
            .finally(() => setLoading(false))
    }, [search])

    const exportCSV = () => {
        window.open(`/api/audit-export${search ? `?policy_id=${search}` : ''}`, '_blank')
    }

    return (
        <div className="p-6 max-w-7xl mx-auto space-y-6">
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <div className="p-2 bg-gray-50 rounded-lg">
                        <ClipboardList className="w-6 h-6 text-gray-600" />
                    </div>
                    <div>
                        <h1 className="text-2xl font-black text-gray-900 tracking-tight">IRDAI Audit Log</h1>
                        <p className="text-sm text-gray-500 font-medium">Immutable agent decision trail for regulatory compliance.</p>
                    </div>
                </div>
                <div className="flex gap-3">
                    <div className="group relative">
                        <input
                            value={search}
                            onChange={e => setSearch(e.target.value)}
                            placeholder="Policy ID..."
                            className="pl-9 pr-4 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500/20 focus:border-teal-500 transition-all w-48 shadow-sm"
                        />
                        <Search className="w-4 h-4 text-gray-400 absolute left-3 top-2.5 group-focus-within:text-teal-500 transition-colors" />
                    </div>
                    <button
                        onClick={exportCSV}
                        className="flex items-center gap-2 px-5 py-2 bg-[#1B4F8A] text-white text-sm font-bold rounded-xl hover:bg-blue-800 transition-all shadow-md active:scale-95"
                    >
                        <Download className="w-4 h-4" /> Export CSV
                    </button>
                </div>
            </div>

            <div className="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="w-full text-left">
                        <thead className="bg-gray-50/50 border-b border-gray-100">
                            <tr>
                                {['Time', 'Policy ID', 'Autonomous Agent', 'Action Executed', 'Evidence / Reasoning', 'Prompt'].map(h => (
                                    <th key={h} className="px-6 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">{h}</th>
                                ))}
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-50">
                            {loading ? (
                                [1, 2, 3, 4, 5].map(i => (
                                    <tr key={i} className="animate-pulse">
                                        <td colSpan={6} className="px-6 py-4 h-12 bg-gray-50/20" />
                                    </tr>
                                ))
                            ) : entries.map((e: any, i: number) => (
                                <tr key={i} className="hover:bg-teal-50/10 transition-colors group">
                                    <td className="px-6 py-4 font-mono text-[11px] text-gray-400 whitespace-nowrap">
                                        {new Date(e.timestamp).toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true })}
                                    </td>
                                    <td className="px-6 py-4 font-mono font-bold text-sm text-teal-800 whitespace-nowrap">{e.policy_id}</td>
                                    <td className="px-6 py-4">
                                        <span className={`px-2.5 py-1 rounded-lg text-[10px] font-black uppercase tracking-tight border shadow-sm ${agentBadge[e.agent_name] || 'bg-gray-100 text-gray-600 border-gray-200'}`}>
                                            {e.agent_name.replace(/_/g, ' ')}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4">
                                        <div className="text-xs font-bold text-gray-700 whitespace-nowrap uppercase tracking-tighter">{e.action}</div>
                                    </td>
                                    <td className="px-6 py-4">
                                        <div className="text-xs text-gray-600 font-medium max-w-md line-clamp-1 group-hover:line-clamp-none transition-all leading-relaxed" title={e.evidence}>
                                            {e.evidence}
                                        </div>
                                    </td>
                                    <td className="px-6 py-4">
                                        <span className="text-[10px] font-black text-gray-400 bg-gray-50 px-2 py-1 rounded border uppercase">{e.prompt_version}</span>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
                {!loading && entries.length === 0 && (
                    <div className="text-center py-20 flex flex-col items-center">
                        <Filter className="w-12 h-12 text-gray-100 mb-4" />
                        <p className="text-gray-400 font-medium">No audit entries found for this criteria.</p>
                    </div>
                )}
            </div>
            <div className="flex items-center justify-between text-xs text-gray-400 font-medium">
                <div className="flex items-center gap-2">
                    <Shield className="w-3 h-3" />
                    Verified IRDAI Compliance Log
                </div>
                <div>Showing {entries.length} recent operations</div>
            </div>
        </div>
    )
}
