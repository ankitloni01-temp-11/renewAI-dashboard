import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'

interface ChannelFunnelProps {
    totalPolicies?: number
    emailSent?: number
    whatsappSent?: number
    voiceCalls?: number
    paid?: number
    escalated?: number
    lapsed?: number
}

export default function ChannelFunnel({
    totalPolicies = 500,
    emailSent = 312,
    whatsappSent = 245,
    voiceCalls = 98,
    paid = 380,
    escalated = 32,
    lapsed = 25
}: ChannelFunnelProps) {
    const data = [
        { name: 'Total Policies', value: totalPolicies, color: '#6366f1' },
        { name: 'Email Sent', value: emailSent, color: '#3b82f6' },
        { name: 'WhatsApp', value: whatsappSent, color: '#22c55e' },
        { name: 'Voice Calls', value: voiceCalls, color: '#a855f7' },
        { name: 'Paid ✓', value: paid, color: '#10b981' },
        { name: 'Escalated', value: escalated, color: '#f59e0b' },
        { name: 'Lapsed', value: lapsed, color: '#ef4444' },
    ]

    return (
        <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data} layout="vertical" margin={{ top: 5, right: 30, left: 80, bottom: 5 }}>
                    <XAxis type="number" tick={{ fill: '#9ca3af', fontSize: 12 }} axisLine={{ stroke: '#374151' }} />
                    <YAxis type="category" dataKey="name" tick={{ fill: '#d1d5db', fontSize: 12 }} axisLine={false} width={90} />
                    <Tooltip
                        contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px', color: '#e5e7eb' }}
                    />
                    <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                        {data.map((entry, i) => (
                            <Cell key={i} fill={entry.color} />
                        ))}
                    </Bar>
                </BarChart>
            </ResponsiveContainer>
        </div>
    )
}
