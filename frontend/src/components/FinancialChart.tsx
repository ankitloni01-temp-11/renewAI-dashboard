import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend, CartesianGrid } from 'recharts'

interface MonthlyData {
    month: string
    cost_saving: number
    revenue_uplift: number
}

interface FinancialChartProps {
    data?: MonthlyData[]
}

const defaultData: MonthlyData[] = [
    { month: 'Oct 2025', cost_saving: 0.8, revenue_uplift: 2.1 },
    { month: 'Nov 2025', cost_saving: 0.9, revenue_uplift: 2.5 },
    { month: 'Dec 2025', cost_saving: 1.0, revenue_uplift: 2.9 },
    { month: 'Jan 2026', cost_saving: 1.075, revenue_uplift: 3.24 },
    { month: 'Feb 2026', cost_saving: 1.075, revenue_uplift: 3.24 },
    { month: 'Mar 2026', cost_saving: 1.075, revenue_uplift: 3.24 },
]

export default function FinancialChart({ data = defaultData }: FinancialChartProps) {
    return (
        <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis dataKey="month" tick={{ fill: '#9ca3af', fontSize: 11 }} axisLine={{ stroke: '#374151' }} />
                    <YAxis tick={{ fill: '#9ca3af', fontSize: 12 }} axisLine={{ stroke: '#374151' }} unit=" Cr" />
                    <Tooltip
                        contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px', color: '#e5e7eb' }}
                        formatter={(value: number) => [`₹${value} Cr`, '']}
                    />
                    <Legend wrapperStyle={{ color: '#d1d5db' }} />
                    <Line type="monotone" dataKey="cost_saving" stroke="#10b981" strokeWidth={2} dot={{ r: 4 }} name="Cost Saving" />
                    <Line type="monotone" dataKey="revenue_uplift" stroke="#6366f1" strokeWidth={2} dot={{ r: 4 }} name="Revenue Uplift" />
                </LineChart>
            </ResponsiveContainer>
        </div>
    )
}
