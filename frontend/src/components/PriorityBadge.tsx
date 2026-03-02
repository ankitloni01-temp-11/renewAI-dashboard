interface PriorityBadgeProps {
    priority: string
}

export default function PriorityBadge({ priority }: PriorityBadgeProps) {
    const p = priority?.toUpperCase() || 'STANDARD'
    const styles: Record<string, string> = {
        URGENT: 'bg-red-600 text-white',
        STANDARD: 'bg-blue-600 text-white',
        COMPLIANCE: 'bg-amber-600 text-white',
    }
    const icons: Record<string, string> = {
        URGENT: '🔴',
        STANDARD: '🔵',
        COMPLIANCE: '🟡',
    }

    return (
        <span className={`inline-flex items-center gap-1 text-xs font-bold px-2.5 py-1 rounded-full ${styles[p] || styles.STANDARD}`}>
            {icons[p] || '🔵'} {p}
        </span>
    )
}
