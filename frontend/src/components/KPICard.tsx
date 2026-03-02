import { TrendingUp, TrendingDown, Minus } from 'lucide-react'

interface KPICardProps {
    title: string
    value: number | string
    baseline?: number | string
    target?: number | string
    unit?: string
    trend?: 'up' | 'down' | 'flat'
    status?: 'on_track' | 'close' | 'behind'
    format?: 'percent' | 'currency' | 'number' | 'score'
}

export default function KPICard({ title, value, baseline, target, unit = '', trend, status = 'on_track', format = 'number' }: KPICardProps) {
    const statusColors = {
        on_track: 'border-emerald-500 bg-emerald-950/30',
        close: 'border-amber-500 bg-amber-950/30',
        behind: 'border-red-500 bg-red-950/30'
    }

    const statusDot = {
        on_track: 'bg-emerald-400',
        close: 'bg-amber-400',
        behind: 'bg-red-400'
    }

    const formatValue = (v: number | string) => {
        if (typeof v === 'string') return v
        switch (format) {
            case 'percent': return `${v}%`
            case 'currency': return `₹${v.toLocaleString('en-IN')}`
            case 'score': return v.toFixed(1)
            default: return v.toLocaleString('en-IN')
        }
    }

    return (
        <div className={`rounded-xl border-l-4 p-5 bg-gray-900/60 backdrop-blur ${statusColors[status]}`}>
            <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-medium text-gray-400 uppercase tracking-wider">{title}</span>
                <span className={`w-2 h-2 rounded-full ${statusDot[status]}`} />
            </div>
            <div className="flex items-end gap-2">
                <span className="text-3xl font-bold text-white">{formatValue(value)}</span>
                {unit && <span className="text-sm text-gray-400 mb-1">{unit}</span>}
                {trend && (
                    <span className="mb-1 ml-auto">
                        {trend === 'up' && <TrendingUp className="w-5 h-5 text-emerald-400" />}
                        {trend === 'down' && <TrendingDown className="w-5 h-5 text-red-400" />}
                        {trend === 'flat' && <Minus className="w-5 h-5 text-gray-400" />}
                    </span>
                )}
            </div>
            {(baseline !== undefined || target !== undefined) && (
                <div className="flex gap-4 mt-3 text-xs text-gray-500">
                    {baseline !== undefined && <span>Baseline: {formatValue(baseline)}</span>}
                    {target !== undefined && <span>Target: {formatValue(target)}</span>}
                </div>
            )}
        </div>
    )
}
