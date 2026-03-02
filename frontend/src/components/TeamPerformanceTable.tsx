import { formatCurrency } from '../utils/formatCurrency'

interface TeamMember {
    name: string
    employee_id?: string
    role?: string
    specialization?: string
    cases_this_week?: number
    avg_resolution_time_hours?: number
    customer_rating?: number
    retained_premium?: number
}

interface TeamPerformanceTableProps {
    team?: TeamMember[]
}

const defaultTeam: TeamMember[] = [
    { name: 'Priya Sharma', role: 'Senior RRM', specialization: 'bereavement', cases_this_week: 12, avg_resolution_time_hours: 1.2, customer_rating: 4.8, retained_premium: 268800 },
    { name: 'Amit Patel', role: 'Senior RRM', specialization: 'hni', cases_this_week: 8, avg_resolution_time_hours: 2.1, customer_rating: 4.6, retained_premium: 540000 },
    { name: 'Sneha Kulkarni', role: 'Senior RRM', specialization: 'high_value', cases_this_week: 10, avg_resolution_time_hours: 1.8, customer_rating: 4.7, retained_premium: 224000 },
    { name: 'Rahul Deshmukh', role: 'Revival Specialist', cases_this_week: 6, avg_resolution_time_hours: 3.5, customer_rating: 4.5, retained_premium: 134400 },
    { name: 'Kavitha Nair', role: 'Compliance Handler', cases_this_week: 4, avg_resolution_time_hours: 4.0, customer_rating: 4.3, retained_premium: 89600 },
]

export default function TeamPerformanceTable({ team = defaultTeam }: TeamPerformanceTableProps) {
    return (
        <div className="overflow-x-auto">
            <table className="w-full text-sm">
                <thead>
                    <tr className="border-b border-gray-700">
                        <th className="text-left py-3 px-3 text-gray-400 font-medium">Specialist</th>
                        <th className="text-left py-3 px-3 text-gray-400 font-medium">Role</th>
                        <th className="text-right py-3 px-3 text-gray-400 font-medium">Cases/Week</th>
                        <th className="text-right py-3 px-3 text-gray-400 font-medium">Avg Resolution</th>
                        <th className="text-right py-3 px-3 text-gray-400 font-medium">Rating</th>
                        <th className="text-right py-3 px-3 text-gray-400 font-medium">Retained Premium</th>
                    </tr>
                </thead>
                <tbody>
                    {team.map((t, i) => (
                        <tr key={t.employee_id || i} className="border-b border-gray-800 hover:bg-gray-800/40">
                            <td className="py-3 px-3 text-gray-200 font-medium">{t.name}</td>
                            <td className="py-3 px-3 text-gray-400 text-xs">
                                {t.role}
                                {t.specialization && <span className="ml-1 px-1.5 py-0.5 bg-gray-700 rounded text-gray-300">{t.specialization}</span>}
                            </td>
                            <td className="py-3 px-3 text-right text-gray-200">{t.cases_this_week || 0}</td>
                            <td className="py-3 px-3 text-right text-gray-300">{t.avg_resolution_time_hours?.toFixed(1) || '-'}h</td>
                            <td className="py-3 px-3 text-right">
                                <span className={`font-semibold ${(t.customer_rating || 0) >= 4.5 ? 'text-emerald-400' : 'text-amber-400'}`}>
                                    ⭐ {t.customer_rating?.toFixed(1) || '-'}
                                </span>
                            </td>
                            <td className="py-3 px-3 text-right text-emerald-300 font-medium">{formatCurrency(t.retained_premium || 0)}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}
