import { useEffect, useState } from 'react'
import { Clock } from 'lucide-react'

interface SLATimerProps {
    escalatedAt: string
    slaHours: number
}

export default function SLATimer({ escalatedAt, slaHours }: SLATimerProps) {
    const [remaining, setRemaining] = useState('')
    const [isOverdue, setIsOverdue] = useState(false)

    useEffect(() => {
        const update = () => {
            const start = new Date(escalatedAt).getTime()
            const deadline = start + slaHours * 3600000
            const now = Date.now()
            const diff = deadline - now

            if (diff <= 0) {
                const overdueMs = Math.abs(diff)
                const h = Math.floor(overdueMs / 3600000)
                const m = Math.floor((overdueMs % 3600000) / 60000)
                setRemaining(`-${h}h ${m}m overdue`)
                setIsOverdue(true)
            } else {
                const h = Math.floor(diff / 3600000)
                const m = Math.floor((diff % 3600000) / 60000)
                const s = Math.floor((diff % 60000) / 1000)
                setRemaining(`${h}h ${m}m ${s}s`)
                setIsOverdue(h === 0 && m < 30)
            }
        }
        update()
        const id = setInterval(update, 1000)
        return () => clearInterval(id)
    }, [escalatedAt, slaHours])

    return (
        <span className={`inline-flex items-center gap-1 text-xs font-mono font-medium px-2 py-1 rounded ${isOverdue ? 'bg-red-900/60 text-red-300' : 'bg-gray-800 text-gray-300'
            }`}>
            <Clock className="w-3 h-3" />
            {remaining}
        </span>
    )
}
