import { useState, useEffect } from 'react'
import { AlertTriangle, X, Loader2 } from 'lucide-react'
import api from '../api/client'
import toast from 'react-hot-toast'
import { useHumanQueue } from '../hooks/useHumanQueue'
import { useQueryClient } from '@tanstack/react-query'

const fmt = (n: number) => '₹' + n.toLocaleString('en-IN')
const borderColor = (p: number) => p >= 0.7 ? 'border-l-red-500' : p >= 0.4 ? 'border-l-yellow-400' : 'border-l-gray-300'
const priorityBadge = (p: number) => p >= 0.7 ? 'bg-red-100 text-red-700' : p >= 0.4 ? 'bg-yellow-100 text-yellow-700' : 'bg-gray-100 text-gray-500'

export default function EscalationPage() {
    const [filter, setFilter] = useState('all')
    const { data: cases = [], isLoading } = useHumanQueue(undefined, filter === 'all' ? undefined : filter)
    const [resolving, setResolving] = useState<any | null>(null)
    const [outcome, setOutcome] = useState('Renewed')
    const [notes, setNotes] = useState('')
    const queryClient = useQueryClient()

    const resolve = async () => {
        if (!resolving) return
        try {
            await api.post(`/api/human-queue/${resolving.case_id}/resolve`, { outcome, notes })
            toast.success(`Case ${resolving.case_id} resolved`)
            setResolving(null); setOutcome('Renewed'); setNotes('')
            queryClient.invalidateQueries({ queryKey: ['queue'] })
        } catch { toast.error('Failed to resolve') }
    }

    return (
        <div className="p-6">
            <div className="flex items-center justify-between mb-5">
                <div className="flex items-center gap-2">
                    <AlertTriangle className="w-5 h-5 text-red-500" />
                    <h1 className="text-xl font-bold text-gray-800">Escalation — Human Queue</h1>
                </div>
                <select value={filter} onChange={e => setFilter(e.target.value)} className="border rounded-lg px-3 py-2 text-sm">
                    <option value="all">All Cases</option>
                    <option value="open">Open</option>
                    <option value="resolved">Resolved</option>
                </select>
            </div>

            <div className="space-y-4">
                {cases.length === 0 && <p className="text-gray-400 text-center py-12">No escalation cases found.</p>}
                {cases.map((c: any) => (
                    <div key={c.case_id} className={`bg-white rounded-xl shadow-sm border border-l-4 ${borderColor(c.priority)} p-5`}>
                        <div className="flex items-start justify-between">
                            <div className="flex-1">
                                <div className="flex items-center gap-2 mb-2">
                                    <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold ${priorityBadge(c.priority)}`}>
                                        PRIORITY {c.priority}
                                    </span>
                                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-gray-800 text-white font-mono">{c.policy_id}</span>
                                    <span className="text-xs text-gray-400">Case #{c.case_id.split('-')[1]}</span>
                                </div>
                                <h3 className="font-bold text-gray-800 text-lg">
                                    {c.customer_name} — {c.product_name} • {fmt(c.premium)}
                                </h3>
                                <p className="text-sm text-gray-500 mt-1">Reason: {c.reason}</p>
                                {c.status === 'resolved' && (
                                    <div className="mt-2 text-xs text-green-600 bg-green-50 px-3 py-1 rounded inline-block">
                                        ✅ Resolved: {c.resolution_outcome}
                                    </div>
                                )}
                            </div>
                            {c.status === 'open' && (
                                <button onClick={() => setResolving(c)} className="px-4 py-2 bg-teal-600 text-white text-sm rounded-lg hover:bg-teal-700 transition-colors flex-shrink-0">
                                    ✓ Resolve
                                </button>
                            )}
                        </div>
                    </div>
                ))}
            </div>

            {/* Resolve Modal */}
            {resolving && (
                <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" onClick={() => setResolving(null)}>
                    <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md" onClick={e => e.stopPropagation()}>
                        <div className="flex items-center justify-between px-6 py-4 border-b">
                            <h2 className="font-bold">Resolve {resolving.case_id}</h2>
                            <button onClick={() => setResolving(null)}><X className="w-5 h-5" /></button>
                        </div>
                        <div className="p-6 space-y-4">
                            <div className="text-sm text-gray-600">
                                <strong>{resolving.customer_name}</strong> — {resolving.product_name} • {fmt(resolving.premium)}
                            </div>
                            <div>
                                <label className="block text-xs font-semibold text-gray-500 mb-1">Outcome</label>
                                <select value={outcome} onChange={e => setOutcome(e.target.value)} className="w-full border rounded-lg px-3 py-2 text-sm">
                                    {['Renewed', 'Premium Holiday', 'Surrendered', 'Callback', 'Declined'].map(o => <option key={o}>{o}</option>)}
                                </select>
                            </div>
                            <div>
                                <label className="block text-xs font-semibold text-gray-500 mb-1">Notes</label>
                                <textarea value={notes} onChange={e => setNotes(e.target.value)} rows={3} className="w-full border rounded-lg px-3 py-2 text-sm" placeholder="Resolution notes..." />
                            </div>
                            <button onClick={resolve} className="w-full py-2.5 bg-teal-600 text-white font-medium rounded-lg hover:bg-teal-700 transition-colors">
                                Confirm Resolution
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}
