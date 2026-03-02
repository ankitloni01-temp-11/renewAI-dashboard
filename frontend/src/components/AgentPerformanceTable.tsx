interface AgentMetrics {
    agent: string
    messages_processed: number
    critique_pass_pct: number
    avg_score: number
    hallucinations: number
    escalations: number
    avg_latency_ms: number
    cost_per_message: number
}

interface AgentPerformanceTableProps {
    agents?: AgentMetrics[]
}

const defaultAgents: AgentMetrics[] = [
    { agent: 'Email Agent', messages_processed: 312, critique_pass_pct: 94.2, avg_score: 8.4, hallucinations: 0, escalations: 3, avg_latency_ms: 820, cost_per_message: 0.02 },
    { agent: 'WhatsApp Agent', messages_processed: 587, critique_pass_pct: 91.8, avg_score: 8.1, hallucinations: 1, escalations: 12, avg_latency_ms: 650, cost_per_message: 0.015 },
    { agent: 'Voice Agent', messages_processed: 198, critique_pass_pct: 89.4, avg_score: 7.9, hallucinations: 0, escalations: 8, avg_latency_ms: 780, cost_per_message: 0.025 },
    { agent: 'Planner', messages_processed: 445, critique_pass_pct: 96.1, avg_score: 8.7, hallucinations: 0, escalations: 2, avg_latency_ms: 920, cost_per_message: 0.03 },
]

export default function AgentPerformanceTable({ agents = defaultAgents }: AgentPerformanceTableProps) {
    return (
        <div className="overflow-x-auto">
            <table className="w-full text-sm">
                <thead>
                    <tr className="border-b border-gray-700">
                        <th className="text-left py-3 px-3 text-gray-400 font-medium">Agent</th>
                        <th className="text-right py-3 px-3 text-gray-400 font-medium">Processed</th>
                        <th className="text-right py-3 px-3 text-gray-400 font-medium">Pass %</th>
                        <th className="text-right py-3 px-3 text-gray-400 font-medium">Avg Score</th>
                        <th className="text-right py-3 px-3 text-gray-400 font-medium">Halluc.</th>
                        <th className="text-right py-3 px-3 text-gray-400 font-medium">Escalations</th>
                        <th className="text-right py-3 px-3 text-gray-400 font-medium">Avg Latency</th>
                        <th className="text-right py-3 px-3 text-gray-400 font-medium">Cost/Msg</th>
                    </tr>
                </thead>
                <tbody>
                    {agents.map(a => (
                        <tr key={a.agent} className="border-b border-gray-800 hover:bg-gray-800/40">
                            <td className="py-3 px-3 text-blue-300 font-medium">{a.agent}</td>
                            <td className="py-3 px-3 text-right text-gray-200">{a.messages_processed}</td>
                            <td className="py-3 px-3 text-right">
                                <span className={a.critique_pass_pct >= 90 ? 'text-emerald-400' : 'text-amber-400'}>{a.critique_pass_pct}%</span>
                            </td>
                            <td className="py-3 px-3 text-right">
                                <span className={a.avg_score >= 8 ? 'text-emerald-400' : a.avg_score >= 7 ? 'text-amber-400' : 'text-red-400'}>{a.avg_score.toFixed(1)}</span>
                            </td>
                            <td className="py-3 px-3 text-right">
                                <span className={a.hallucinations === 0 ? 'text-emerald-400' : 'text-red-400'}>{a.hallucinations}</span>
                            </td>
                            <td className="py-3 px-3 text-right text-gray-300">{a.escalations}</td>
                            <td className="py-3 px-3 text-right text-gray-300">{a.avg_latency_ms}ms</td>
                            <td className="py-3 px-3 text-right text-gray-400">${a.cost_per_message}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}
