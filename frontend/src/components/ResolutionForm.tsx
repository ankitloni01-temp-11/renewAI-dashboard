import { useState } from 'react'
import { CheckCircle, PauseCircle, ArrowUpCircle } from 'lucide-react'

interface ResolutionFormProps {
    onResolve: (resolution: string, notes: string) => void
    onHold?: () => void
    onReescalate?: (team: string) => void
}

const resolutionOptions = [
    'Renewed – payment collected',
    'Premium holiday granted',
    'Revival fee waived',
    'Death benefit claim initiated',
    'Customer chose to surrender',
    'Customer chose to lapse – informed decision',
    'Escalated further',
    'Other',
]

export default function ResolutionForm({ onResolve, onHold, onReescalate }: ResolutionFormProps) {
    const [selected, setSelected] = useState('')
    const [notes, setNotes] = useState('')

    return (
        <div className="bg-gray-800/60 rounded-xl p-5 border border-gray-700">
            <h3 className="text-lg font-semibold text-white mb-4">Resolution</h3>

            <div className="space-y-2 mb-4">
                {resolutionOptions.map(opt => (
                    <label key={opt} className={`flex items-center gap-3 p-2.5 rounded-lg cursor-pointer transition-colors ${selected === opt ? 'bg-blue-900/40 border border-blue-600' : 'hover:bg-gray-700/40 border border-transparent'
                        }`}>
                        <input
                            type="radio" name="resolution" value={opt}
                            checked={selected === opt}
                            onChange={(e) => setSelected(e.target.value)}
                            className="accent-blue-500"
                        />
                        <span className="text-sm text-gray-200">{opt}</span>
                    </label>
                ))}
            </div>

            <textarea
                value={notes} onChange={(e) => setNotes(e.target.value)}
                placeholder="Resolution notes for the audit trail..."
                rows={3}
                className="w-full bg-gray-900 border border-gray-600 rounded-lg p-3 text-sm text-gray-200 placeholder-gray-500 mb-4 focus:border-blue-500 focus:outline-none"
            />

            <div className="flex gap-3">
                <button
                    onClick={() => selected && onResolve(selected, notes)}
                    disabled={!selected}
                    className="flex items-center gap-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 disabled:bg-gray-600 disabled:cursor-not-allowed rounded-lg text-sm font-medium text-white transition-colors"
                >
                    <CheckCircle size={16} /> RESOLVE CASE
                </button>
                {onHold && (
                    <button onClick={onHold} className="flex items-center gap-2 px-4 py-2 bg-amber-600 hover:bg-amber-500 rounded-lg text-sm font-medium text-white transition-colors">
                        <PauseCircle size={16} /> PUT ON HOLD
                    </button>
                )}
                {onReescalate && (
                    <button onClick={() => onReescalate('senior_management')} className="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-500 rounded-lg text-sm font-medium text-white transition-colors">
                        <ArrowUpCircle size={16} /> RE-ESCALATE
                    </button>
                )}
            </div>
        </div>
    )
}
