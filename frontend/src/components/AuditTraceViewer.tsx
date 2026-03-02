import { useState } from 'react'
import { ChevronDown, ChevronRight, CheckCircle, XCircle, RefreshCw } from 'lucide-react'
import CritiqueBadge from './CritiqueBadge'
import type { AuditEntry } from '../types'
import { formatDate } from '../utils/formatDate'

interface AuditTraceViewerProps {
    entries: AuditEntry[]
}

export default function AuditTraceViewer({ entries }: AuditTraceViewerProps) {
    const [expanded, setExpanded] = useState<Set<number>>(new Set())

    const toggle = (i: number) => {
        const next = new Set(expanded)
        next.has(i) ? next.delete(i) : next.add(i)
        setExpanded(next)
    }

    if (!entries || entries.length === 0) {
        return <div className="text-gray-500 text-sm py-4 text-center">No audit trail entries.</div>
    }

    const stepColor = (verdict?: string) => {
        if (!verdict) return 'border-gray-600'
        const v = verdict.toUpperCase()
        if (v === 'APPROVED' || v === 'PASS') return 'border-emerald-500'
        if (v === 'REJECTED' || v === 'FAIL') return 'border-red-500'
        return 'border-amber-500'
    }

    const stepIcon = (verdict?: string) => {
        if (!verdict) return <RefreshCw size={14} className="text-gray-400" />
        const v = verdict.toUpperCase()
        if (v === 'APPROVED' || v === 'PASS') return <CheckCircle size={14} className="text-emerald-400" />
        if (v === 'REJECTED' || v === 'FAIL') return <XCircle size={14} className="text-red-400" />
        return <RefreshCw size={14} className="text-amber-400" />
    }

    return (
        <div className="space-y-2">
            {entries.map((entry, i) => (
                <div key={entry.trace_id || i} className={`border-l-2 ${stepColor(entry.verdict)} bg-gray-800/40 rounded-r-lg`}>
                    <button onClick={() => toggle(i)} className="w-full flex items-center gap-3 p-3 text-left hover:bg-gray-700/30 transition-colors">
                        {expanded.has(i) ? <ChevronDown size={14} className="text-gray-400" /> : <ChevronRight size={14} className="text-gray-400" />}
                        <span className="text-xs font-mono text-gray-500 w-6">#{entry.step_number}</span>
                        {stepIcon(entry.verdict)}
                        <span className="text-sm font-medium text-blue-300">{entry.agent_name}</span>
                        <span className="text-xs text-gray-400 flex-1 truncate">{entry.action}</span>
                        {entry.critique_score !== undefined && <CritiqueBadge score={entry.critique_score} />}
                        {entry.latency_ms !== undefined && <span className="text-xs text-gray-500">{entry.latency_ms}ms</span>}
                        <span className="text-xs text-gray-500">{formatDate(entry.timestamp)}</span>
                    </button>

                    {expanded.has(i) && (
                        <div className="px-4 pb-4 text-xs">
                            <div className="grid grid-cols-2 gap-2 mb-3">
                                <div><span className="text-gray-500">Model:</span> <span className="text-gray-300">{entry.model_used || 'N/A'}</span></div>
                                <div><span className="text-gray-500">Tokens:</span> <span className="text-gray-300">{entry.token_count_in || 0} in / {entry.token_count_out || 0} out</span></div>
                            </div>
                            {entry.input_summary && (
                                <div className="mb-2">
                                    <span className="text-gray-500 font-medium">Input:</span>
                                    <pre className="mt-1 p-2 bg-gray-900 rounded text-gray-300 overflow-x-auto whitespace-pre-wrap">{entry.input_summary}</pre>
                                </div>
                            )}
                            {entry.output_summary && (
                                <div className="mb-2">
                                    <span className="text-gray-500 font-medium">Output:</span>
                                    <pre className="mt-1 p-2 bg-gray-900 rounded text-gray-300 overflow-x-auto whitespace-pre-wrap">{entry.output_summary}</pre>
                                </div>
                            )}
                            {entry.full_output && (
                                <details className="mt-2">
                                    <summary className="text-gray-500 cursor-pointer hover:text-gray-300">Full JSON output</summary>
                                    <pre className="mt-1 p-2 bg-gray-900 rounded text-gray-400 overflow-x-auto text-xs whitespace-pre-wrap">{JSON.stringify(entry.full_output, null, 2)}</pre>
                                </details>
                            )}
                        </div>
                    )}
                </div>
            ))}
        </div>
    )
}
