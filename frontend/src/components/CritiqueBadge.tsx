interface CritiqueBadgeProps {
    score?: number
    verdict?: string
}

export default function CritiqueBadge({ score, verdict }: CritiqueBadgeProps) {
    if (score === undefined && !verdict) return null

    const color = !score ? 'bg-gray-700 text-gray-300'
        : score >= 7 ? 'bg-emerald-900/60 text-emerald-300'
            : score >= 5 ? 'bg-amber-900/60 text-amber-300'
                : 'bg-red-900/60 text-red-300'

    return (
        <span className={`inline-flex items-center gap-1 text-xs font-medium px-2 py-0.5 rounded ${color}`}>
            {score !== undefined && <span>{score.toFixed(1)}/10</span>}
            {verdict && <span className="opacity-70">• {verdict}</span>}
        </span>
    )
}
