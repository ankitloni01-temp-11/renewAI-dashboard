import { useState, useEffect } from 'react'
import { Search, Play, Eye, X, Check, Loader2, Shield, Activity } from 'lucide-react'
import api from '../api/client'
import { useUIStore } from '../stores/uiStore'

const SEGMENTS = ['All Segments', 'Senior Citizen', 'Middle Income', 'Budget Conscious', 'Young Professional', 'Wealth Builder']
const STATUSES = ['All Statuses', 'OVERDUE', 'ACTIVE', 'LAPSED', 'PAID', 'ESCALATED']
const segmentColors: Record<string, string> = {
    'Senior Citizen': 'bg-gray-800 text-white', 'Middle Income': 'bg-gray-500 text-white',
    'Budget Conscious': 'bg-gray-700 text-white', 'Young Professional': 'bg-gray-400 text-gray-900',
    'Wealth Builder': 'bg-gray-900 text-white',
}
const statusColors: Record<string, string> = {
    OVERDUE: 'text-red-600 bg-red-50', ACTIVE: 'text-green-600 bg-green-50',
    LAPSED: 'text-orange-500 bg-orange-50', PAID: 'text-green-700 bg-green-100',
    ESCALATED: 'text-red-700 bg-red-100',
}
const fmt = (n: number) => '₹' + n.toLocaleString('en-IN')
const fmtDate = (d: string) => {
    const dt = new Date(d); const m = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return `${dt.getDate()} ${m[dt.getMonth()]} ${String(dt.getFullYear()).slice(2)}`
}

interface TraceEntry { timestamp: string; policy_id: string; agent_name: string; action: string; evidence: string; prompt_version: string }
interface WorkflowStep { name: string; label: string; state: 'pending' | 'active' | 'done'; result?: string }

const agentColor = (name: string) => {
    const n = name.toLowerCase()
    if (n.includes('orchestrator')) return '#2dd4a8'
    if (n.includes('planner')) return '#f59e0b'
    if (n.includes('critique')) return '#f59e0b'
    if (n.includes('safety')) return '#22c55e'
    return '#2dd4a8'
}

export default function PoliciesPage() {
    const [policies, setPolicies] = useState<any[]>([])
    const [search, setSearch] = useState('')
    const [segment, setSegment] = useState('All Segments')
    const [status, setStatus] = useState('All Statuses')
    const [tracePolicy, setTracePolicy] = useState<string | null>(null)
    const [traceData, setTraceData] = useState<TraceEntry[]>([])
    const { setGlobalTriggerPolicy } = useUIStore()

    useEffect(() => {
        api.get('/api/policies', { params: { segment: segment === 'All Segments' ? undefined : segment, status: status === 'All Statuses' ? undefined : status, search: search || undefined } })
            .then(r => setPolicies(r.data)).catch(() => { })
    }, [search, segment, status])

    const openTrace = (pid: string) => {
        setTracePolicy(pid)
        api.get(`/api/audit/${pid}`).then(r => setTraceData(r.data)).catch(() => setTraceData([]))
    }

    const openTrigger = (pol: any) => {
        // Just set the global trigger policy, the GlobalIntelligencePipeline component handles the rest.
        setGlobalTriggerPolicy(pol)
        api.post('/api/triggers/start-journey', { policy_id: pol.policy_id }).catch(() => { })
    }

    return (
        <div className="p-6">
            <div className="flex items-center justify-between mb-5">
                <h1 className="text-xl font-bold text-gray-800">Policies</h1>
                <div className="flex gap-3">
                    <div className="relative">
                        <Search className="absolute left-3 top-2.5 w-4 h-4 text-gray-400" />
                        <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search policy / customer..."
                            className="pl-9 pr-3 py-2 border rounded-lg text-sm w-64 focus:outline-none focus:ring-2 focus:ring-teal-400" />
                    </div>
                    <select value={segment} onChange={e => setSegment(e.target.value)} className="border rounded-lg px-3 py-2 text-sm">
                        {SEGMENTS.map(s => <option key={s}>{s}</option>)}
                    </select>
                    <select value={status} onChange={e => setStatus(e.target.value)} className="border rounded-lg px-3 py-2 text-sm">
                        {STATUSES.map(s => <option key={s}>{s}</option>)}
                    </select>
                </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
                <table className="w-full text-sm">
                    <thead className="bg-gray-50 border-b">
                        <tr>{['Policy ID', 'Customer', 'Type', 'Segment', 'Premium', 'Due Date', 'Status', 'Actions'].map(h =>
                            <th key={h} className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">{h}</th>
                        )}</tr>
                    </thead>
                    <tbody className="divide-y">
                        {policies.map((p: any) => (
                            <tr key={p.policy_id} className="hover:bg-gray-50 transition-colors">
                                <td className="px-4 py-3 font-mono text-xs font-bold text-teal-700">{p.policy_id}</td>
                                <td className="px-4 py-3">
                                    <div className="font-medium text-gray-800">{p.customer?.name}</div>
                                    <div className="text-xs text-gray-400">{p.customer?.email}</div>
                                </td>
                                <td className="px-4 py-3 text-xs">{p.product_name}</td>
                                <td className="px-4 py-3">
                                    <span className={`text-[10px] px-2 py-0.5 rounded-full font-medium ${segmentColors[p.customer?.segment] || 'bg-gray-200'}`}>
                                        {p.customer?.segment}
                                    </span>
                                </td>
                                <td className="px-4 py-3 font-medium">{fmt(p.premium)}</td>
                                <td className="px-4 py-3 text-xs text-gray-500">{fmtDate(p.due_date)}</td>
                                <td className="px-4 py-3">
                                    <span className={`text-[11px] px-2 py-0.5 rounded font-bold ${statusColors[p.effective_status] || 'text-gray-500 bg-gray-100'}`}>
                                        {p.effective_status}
                                    </span>
                                </td>
                                <td className="px-4 py-3">
                                    <div className="flex gap-2">
                                        <button type="button" onClick={() => openTrigger(p)} className="flex items-center gap-1 px-3 py-1.5 bg-[#1B4F8A] text-white text-xs rounded-lg hover:bg-blue-800 transition-colors">
                                            <Play className="w-3 h-3" /> Trigger
                                        </button>
                                        <button type="button" onClick={() => openTrace(p.policy_id)} className="flex items-center gap-1 px-3 py-1.5 border border-gray-300 text-gray-600 text-xs rounded-lg hover:bg-gray-50 transition-colors">
                                            <Eye className="w-3 h-3" /> Trace
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Trace Modal */}
            {tracePolicy && (
                <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" onClick={() => setTracePolicy(null)}>
                    <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[80vh] overflow-hidden" onClick={e => e.stopPropagation()}>
                        <div className="flex items-center justify-between px-6 py-4 border-b bg-gray-50">
                            <h2 className="font-bold text-lg">🔍 Trace: {tracePolicy}</h2>
                            <button type="button" onClick={() => setTracePolicy(null)} className="p-1 hover:bg-gray-200 rounded"><X className="w-5 h-5" /></button>
                        </div>
                        <div className="overflow-y-auto max-h-[65vh] p-6 space-y-4">
                            {traceData.length === 0 && <p className="text-gray-400 text-center py-8">No trace data available for this policy.</p>}
                            {traceData.map((e, i) => (
                                <div key={i} className="flex gap-4">
                                    <div className="text-xs text-gray-400 w-20 flex-shrink-0 pt-0.5 font-mono">
                                        {new Date(e.timestamp).toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                                    </div>
                                    <div className="flex-1">
                                        <div className="font-bold text-xs mb-1" style={{ color: agentColor(e.agent_name) }}>{e.agent_name.toUpperCase()}</div>
                                        <div className="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap bg-gray-50 rounded-lg p-3">{e.evidence}</div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}
