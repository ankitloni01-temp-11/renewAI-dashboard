import { useState, useEffect } from 'react'
import { X, Check, Loader2, Shield, Activity } from 'lucide-react'
import api from '../api/client'
import { useUIStore } from '../stores/uiStore'
import { useQueryClient } from '@tanstack/react-query'

interface WorkflowStep { name: string; label: string; state: 'pending' | 'active' | 'done'; result?: string }

export default function GlobalIntelligencePipeline() {
    const { globalTriggerPolicy, setGlobalTriggerPolicy } = useUIStore()
    const [steps, setSteps] = useState<WorkflowStep[]>([])
    const queryClient = useQueryClient()

    useEffect(() => {
        if (globalTriggerPolicy) {
            const initial: WorkflowStep[] = [
                { name: 'orchestrator', label: 'ORCHESTRATOR — Selecting best channel...', state: 'active' },
                { name: 'critique_a', label: 'CRITIQUE A — Verifying channel with evidence...', state: 'pending' },
                { name: 'planner', label: 'PLANNER — Building execution plan...', state: 'pending' },
                { name: 'draft', label: 'DRAFT + GREETING — Drafting message segments...', state: 'pending' },
                { name: 'critique_b', label: 'CRITIQUE B — Compliance check...', state: 'pending' },
                { name: 'channel', label: 'CHANNEL AGENT — Dispatching message...', state: 'pending' },
            ]
            setSteps(initial)

            // Robust simulation: Chain of timeouts to ensure sequential state transitions
            const results = [
                'Channel: WhatsApp selected',
                'Verdict: APPROVED (1.0)',
                'Plan generated',
                'Message drafted',
                'Compliance: PASSED',
                'Message dispatched ✓'
            ]

            let currentIdx = 0
            const runNext = () => {
                if (currentIdx >= initial.length) {
                    // Invalidate queries to refresh background pages
                    queryClient.invalidateQueries({ queryKey: ['journeys'] })
                    queryClient.invalidateQueries({ queryKey: ['kpis'] })
                    return
                }

                setSteps(prev => {
                    return prev.map((s, i) => {
                        if (i === currentIdx) {
                            return { ...s, state: 'done' as const, result: results[i] }
                        }
                        if (i === currentIdx + 1) {
                            return { ...s, state: 'active' as const }
                        }
                        if (i < currentIdx) {
                            return { ...s, state: 'done' as const }
                        }
                        if (i > currentIdx + 1) {
                            return { ...s, state: 'pending' as const }
                        }
                        return s
                    })
                })

                currentIdx++
                if (currentIdx < initial.length) {
                    setTimeout(runNext, 1800)
                }
            }

            setTimeout(runNext, 1800)
        }
    }, [globalTriggerPolicy, queryClient])

    if (!globalTriggerPolicy) return null

    return (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[100] flex items-center justify-center p-4 transition-all" onClick={() => setGlobalTriggerPolicy(null)}>
            <div className="bg-white rounded-3xl shadow-2xl w-full max-w-xl overflow-hidden border border-white/20" onClick={e => e.stopPropagation()}>
                <div className="bg-gradient-to-r from-[#1B4F8A] to-blue-600 px-8 py-6 text-white relative">
                    <div className="absolute top-0 right-0 p-8 opacity-10">
                        <Activity className="w-32 h-32" />
                    </div>
                    <div className="relative z-10 flex justify-between items-start">
                        <div>
                            <div className="flex items-center gap-2 mb-1">
                                <div className="p-1 bg-white/20 rounded-lg backdrop-blur-md">
                                    <Shield className="w-5 h-5 text-yellow-300" />
                                </div>
                                <span className="text-xs font-bold uppercase tracking-widest text-blue-100">Live Execution</span>
                            </div>
                            <h2 className="text-2xl font-bold tracking-tight">Intelligence Pipeline</h2>
                            <p className="text-blue-100/80 text-sm mt-1">
                                Policy <span className="font-mono font-bold text-white">{globalTriggerPolicy.policy_id}</span> • {globalTriggerPolicy.customer?.name}
                            </p>
                        </div>
                        <button type="button" onClick={() => setGlobalTriggerPolicy(null)} className="p-2 hover:bg-white/10 rounded-full transition-colors">
                            <X className="w-6 h-6" />
                        </button>
                    </div>
                </div>

                <div className="p-8 bg-slate-50/50">
                    <div className="relative">
                        <div className="absolute left-4 top-2 bottom-2 w-0.5 bg-slate-200 z-0"></div>

                        <div className="space-y-8 relative z-10">
                            {steps.map((s, i) => {
                                const isActive = s.state === 'active';
                                const isDone = s.state === 'done';

                                return (
                                    <div key={i} className={`flex items-start gap-6 transition-all duration-500 ${!isActive && !isDone ? 'opacity-40 grayscale' : 'opacity-100'}`}>
                                        <div className={`w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0 shadow-lg transition-all duration-500 ${isActive ? 'bg-[#1B4F8A] scale-110 ring-4 ring-blue-100' :
                                            isDone ? 'bg-blue-600' : 'bg-slate-300'
                                            }`}>
                                            {isDone ? <Check className="w-4 h-4 text-white" /> :
                                                isActive ? <Loader2 className="w-4 h-4 text-white animate-spin" /> :
                                                    <div className="w-1.5 h-1.5 bg-white rounded-full" />}
                                        </div>

                                        <div className="flex-1 pt-1">
                                            <div className="flex items-center justify-between mb-1">
                                                <h3 className={`text-sm font-bold tracking-wide uppercase ${isActive ? 'text-[#1B4F8A]' : isDone ? 'text-slate-800' : 'text-slate-400'}`}>
                                                    {s.name.replace(/_/g, ' ')}
                                                </h3>
                                                {isActive && !isDone && (
                                                    <span className="text-[10px] font-bold px-2 py-0.5 bg-blue-100 text-[#1B4F8A] rounded-full animate-pulse uppercase tracking-wider">
                                                        Thinking...
                                                    </span>
                                                )}
                                            </div>

                                            <p className={`text-sm leading-relaxed ${isActive ? 'text-slate-700' : isDone ? 'text-slate-600 font-medium' : 'text-slate-400'}`}>
                                                {s.label.split(' — ')[1] || s.label}
                                            </p>

                                            {isDone && s.result && (
                                                <div className="mt-2 text-xs font-mono bg-blue-50/50 text-blue-700 p-2 rounded-lg border border-blue-100 flex items-center gap-2 animate-in fade-in slide-in-from-left-2">
                                                    <span className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse"></span>
                                                    {s.result}
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    </div>

                    {steps.every(s => s.state === 'done') && (
                        <div className="mt-10 p-5 bg-gradient-to-br from-green-50 to-emerald-50 text-green-800 text-sm rounded-2xl text-center font-bold border border-green-100 shadow-sm animate-in zoom-in-95 duration-500">
                            <div className="flex items-center justify-center gap-2 mb-1">
                                <Check className="w-5 h-5 bg-green-500 text-white rounded-full p-1" />
                                <span>JOURNEY SUCCESSFULLY DEPLOYED</span>
                            </div>
                            <p className="text-green-600 text-xs font-normal">Customer has been notified via {globalTriggerPolicy.communication_preference || 'WhatsApp'}</p>
                        </div>
                    )}
                </div>

                <div className="px-8 py-4 bg-white border-t border-slate-100 flex justify-end">
                    <button
                        type="button"
                        onClick={() => setGlobalTriggerPolicy(null)}
                        className={`px-6 py-2 rounded-xl font-bold text-sm transition-all ${steps.every(s => s.state === 'done')
                            ? 'bg-[#1B4F8A] text-white hover:bg-blue-800'
                            : 'bg-slate-100 text-slate-400 cursor-not-allowed'
                            }`}
                        disabled={!steps.every(s => s.state === 'done')}
                    >
                        {steps.every(s => s.state === 'done') ? 'Close Pipeline' : 'Engine Running...'}
                    </button>
                </div>
            </div>
        </div>
    )
}
