import KPICard from './KPICard'
import type { KPIs } from '../types'

interface KPIScorecardProps {
    kpis: KPIs
}

const kpiConfig = [
    { key: 'persistency_rate', title: '13th Month Persistency', baseline: 71, target: 88, format: 'percent' as const, goodDirection: 'up' as const },
    { key: 'cost_per_renewal', title: 'Cost per Renewal', baseline: 182, target: 45, format: 'currency' as const, goodDirection: 'down' as const },
    { key: 'email_open_rate', title: 'Email Open Rate', baseline: 18, target: 42, format: 'percent' as const, goodDirection: 'up' as const },
    { key: 'whatsapp_response_rate', title: 'WhatsApp Response Rate', baseline: 0, target: 58, format: 'percent' as const, goodDirection: 'up' as const },
    { key: 'voice_conversion_rate', title: 'Voice Conversion Rate', baseline: 0, target: 31, format: 'percent' as const, goodDirection: 'up' as const },
    { key: 'human_escalation_rate', title: 'Human Escalation Rate', baseline: 100, target: 10, format: 'percent' as const, goodDirection: 'down' as const },
    { key: 'customer_nps', title: 'Customer NPS', baseline: 34, target: 55, format: 'score' as const, goodDirection: 'up' as const },
    { key: 'irdai_violations', title: 'IRDAI Violations', baseline: 12, target: 0, format: 'number' as const, goodDirection: 'down' as const },
    { key: 'ai_accuracy_score', title: 'AI Accuracy Score', baseline: 0, target: 87, format: 'percent' as const, goodDirection: 'up' as const },
    { key: 'distress_escalation_pct', title: 'Distress Escalated <2h', baseline: 0, target: 100, format: 'percent' as const, goodDirection: 'up' as const },
]

function getStatus(value: number, target: number, goodDir: 'up' | 'down'): 'on_track' | 'close' | 'behind' {
    const diff = goodDir === 'up' ? value - target : target - value
    if (diff >= 0) return 'on_track'
    if (Math.abs(diff) <= target * 0.15) return 'close'
    return 'behind'
}

export default function KPIScorecard({ kpis }: KPIScorecardProps) {
    return (
        <div className="overflow-x-auto">
            <table className="w-full text-sm">
                <thead>
                    <tr className="border-b border-gray-700">
                        <th className="text-left py-3 px-4 text-gray-400 font-medium">Metric</th>
                        <th className="text-right py-3 px-4 text-gray-400 font-medium">Baseline</th>
                        <th className="text-right py-3 px-4 text-gray-400 font-medium">Target</th>
                        <th className="text-right py-3 px-4 text-gray-400 font-medium">Actual</th>
                        <th className="text-center py-3 px-4 text-gray-400 font-medium">Status</th>
                    </tr>
                </thead>
                <tbody>
                    {kpiConfig.map(cfg => {
                        const value = (kpis as unknown as Record<string, number>)[cfg.key] ?? 0
                        const status = getStatus(value, cfg.target, cfg.goodDirection)
                        const statusColor = { on_track: 'text-emerald-400', close: 'text-amber-400', behind: 'text-red-400' }[status]
                        const dot = { on_track: 'bg-emerald-400', close: 'bg-amber-400', behind: 'bg-red-400' }[status]
                        return (
                            <tr key={cfg.key} className="border-b border-gray-800 hover:bg-gray-800/40">
                                <td className="py-3 px-4 text-gray-200">{cfg.title}</td>
                                <td className="py-3 px-4 text-right text-gray-500">{cfg.format === 'currency' ? `₹${cfg.baseline}` : cfg.baseline}{cfg.format === 'percent' ? '%' : ''}</td>
                                <td className="py-3 px-4 text-right text-gray-400">{cfg.format === 'currency' ? `₹${cfg.target}` : cfg.target}{cfg.format === 'percent' ? '%' : ''}</td>
                                <td className={`py-3 px-4 text-right font-semibold ${statusColor}`}>{cfg.format === 'currency' ? `₹${value}` : value}{cfg.format === 'percent' ? '%' : ''}</td>
                                <td className="py-3 px-4 text-center"><span className={`inline-block w-2.5 h-2.5 rounded-full ${dot}`} /></td>
                            </tr>
                        )
                    })}
                </tbody>
            </table>
        </div>
    )
}
