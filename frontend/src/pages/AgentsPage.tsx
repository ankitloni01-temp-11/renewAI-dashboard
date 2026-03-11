import { useState, useEffect } from 'react'
import { Bot, Compass, Map, Mail, MessageSquare, Phone, ShieldCheck, FileCheck, Shield, Send, Activity } from 'lucide-react'
import api from '../api/client'

const iconMap: Record<string, any> = {
    'Compass': Compass,
    'Map': Map,
    'Mail': Mail,
    'MessageSquare': MessageSquare,
    'Phone': Phone,
    'ShieldCheck': ShieldCheck,
    'FileCheck': FileCheck,
    'Shield': Shield,
    'Send': Send,
    'Activity': Activity
}

export default function AgentsPage() {
    const [agents, setAgents] = useState<any[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        api.get('/api/agents/stats')
            .then(r => setAgents(r.data))
            .catch(() => { })
            .finally(() => setLoading(false))
    }, [])

    return (
        <div className="p-6 max-w-7xl mx-auto space-y-6">
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <div className="p-2 bg-teal-50 rounded-lg">
                        <Bot className="w-6 h-6 text-teal-600" />
                    </div>
                    <div>
                        <h1 className="text-2xl font-black text-gray-900 tracking-tight">AI Agent Fleet</h1>
                        <p className="text-sm text-gray-500 font-medium">Real-time performance metrics for autonomous renewal agents.</p>
                    </div>
                </div>
                <div className="flex items-center gap-2 px-3 py-1 bg-green-50 text-green-700 rounded-full text-xs font-bold ring-1 ring-green-200">
                    <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                    {agents.length} AGENTS ACTIVE
                </div>
            </div>

            {loading ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {[1, 2, 3, 4, 5, 6].map(i => (
                        <div key={i} className="bg-white rounded-2xl shadow-sm border p-6 h-48 animate-pulse" />
                    ))}
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {agents.map((a: any) => {
                        const Icon = iconMap[a.icon] || Bot
                        return (
                            <div key={a.name} className="bg-white rounded-2xl shadow-sm border p-6 hover:shadow-lg transition-all border-gray-100 group">
                                <div className="flex items-start justify-between mb-4">
                                    <div className="w-12 h-12 bg-gray-50 group-hover:bg-teal-50 rounded-xl flex items-center justify-center transition-colors">
                                        <Icon className="w-6 h-6 text-gray-400 group-hover:text-teal-600 transition-colors" />
                                    </div>
                                    <div className="text-[10px] font-bold text-teal-600 bg-teal-50 px-2 py-0.5 rounded uppercase tracking-widest">
                                        Active
                                    </div>
                                </div>
                                <div className="mb-5">
                                    <h3 className="font-black text-gray-800 text-lg leading-tight mb-1">{a.name}</h3>
                                    <p className="text-xs text-gray-500 font-medium leading-relaxed">{a.description}</p>
                                </div>
                                <div className="grid grid-cols-3 gap-3 border-t pt-4 border-gray-50">
                                    {Object.entries(a.stats || {}).map(([key, value]) => (
                                        <div key={key} className="text-center">
                                            <div className="text-sm font-black text-gray-900">
                                                {typeof value === 'number' ?
                                                    (String(value).includes('.') ? (value as number).toFixed(1) : value.toLocaleString()) :
                                                    String(value)}
                                                {key.includes('rate') || key.includes('accuracy') || key.includes('score') && typeof value === 'number' ? '%' : ''}
                                            </div>
                                            <div className="text-[9px] text-gray-400 font-bold uppercase tracking-tighter mt-0.5">
                                                {key.replace(/_/g, ' ')}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )
                    })}
                </div>
            )}
        </div>
    )
}
