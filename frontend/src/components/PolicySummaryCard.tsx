import type { Policy, Customer } from '../types'
import { formatCurrency } from '../utils/formatCurrency'

interface PolicySummaryCardProps {
    policy: Policy
    customer?: Customer
}

export default function PolicySummaryCard({ policy, customer }: PolicySummaryCardProps) {
    const dueDate = policy.due_date ? new Date(policy.due_date) : null
    const daysLeft = dueDate ? Math.ceil((dueDate.getTime() - Date.now()) / 86400000) : null

    return (
        <div className="bg-gray-800/60 rounded-xl p-5 border border-gray-700">
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">Policy Summary</h3>
                <span className={`text-xs font-medium px-2 py-1 rounded ${policy.status === 'active' ? 'bg-emerald-900/50 text-emerald-300' :
                        policy.status === 'lapsed' ? 'bg-red-900/50 text-red-300' : 'bg-gray-700 text-gray-300'
                    }`}>{policy.status?.toUpperCase()}</span>
            </div>

            <div className="grid grid-cols-2 gap-3 text-sm">
                <div><span className="text-gray-400">Policy No:</span> <span className="text-white font-mono">{policy.policy_id}</span></div>
                <div><span className="text-gray-400">Product:</span> <span className="text-white">{policy.product_name}</span></div>
                <div><span className="text-gray-400">Type:</span> <span className="text-white capitalize">{policy.product_type}</span></div>
                <div><span className="text-gray-400">Premium:</span> <span className="text-white font-semibold">{formatCurrency(policy.premium_amount)}</span></div>
                <div><span className="text-gray-400">Sum Assured:</span> <span className="text-white">{formatCurrency(policy.sum_assured)}</span></div>
                <div>
                    <span className="text-gray-400">Due Date:</span>{' '}
                    <span className={`font-medium ${daysLeft !== null && daysLeft < 10 ? 'text-red-400' : 'text-white'}`}>
                        {policy.due_date} {daysLeft !== null && `(${daysLeft}d)`}
                    </span>
                </div>
                {customer && <>
                    <div><span className="text-gray-400">Customer:</span> <span className="text-white">{customer.full_name || customer.name}</span></div>
                    <div><span className="text-gray-400">Tenure:</span> <span className="text-white">{customer.tenure_years} years</span></div>
                </>}
                {policy.fund_value !== undefined && (
                    <div><span className="text-gray-400">Fund Value:</span> <span className="text-white">{formatCurrency(policy.fund_value)}</span></div>
                )}
                {policy.nav_change_pct !== undefined && (
                    <div><span className="text-gray-400">NAV Change:</span> <span className={policy.nav_change_pct >= 0 ? 'text-emerald-400' : 'text-red-400'}>
                        {policy.nav_change_pct > 0 ? '+' : ''}{policy.nav_change_pct}%
                    </span></div>
                )}
            </div>

            {policy.payment_history && policy.payment_history.length > 0 && (
                <div className="mt-4">
                    <span className="text-xs text-gray-400">Payment History:</span>
                    <div className="flex gap-1 mt-1">
                        {policy.payment_history.map((ph, i) => (
                            <span key={i} className={`w-3 h-3 rounded-full ${ph.status === 'on_time' ? 'bg-emerald-500' :
                                    ph.status?.startsWith('late') ? 'bg-amber-500' : 'bg-red-500'
                                }`} title={`${ph.year}: ${ph.status}`} />
                        ))}
                    </div>
                </div>
            )}
        </div>
    )
}
