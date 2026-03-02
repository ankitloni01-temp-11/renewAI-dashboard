import ReactMarkdown from 'react-markdown'

interface BriefingNoteProps {
    note: string
    recommendedApproach?: string
}

export default function BriefingNote({ note, recommendedApproach }: BriefingNoteProps) {
    return (
        <div className="bg-gray-800/60 rounded-xl p-5 border border-gray-700">
            <h3 className="text-lg font-semibold text-white mb-3">🤖 AI Recommended Approach</h3>
            {recommendedApproach && (
                <div className="bg-blue-900/30 border border-blue-700 rounded-lg p-3 mb-4">
                    <p className="text-blue-200 text-sm font-medium">{recommendedApproach}</p>
                </div>
            )}
            <div className="prose prose-sm prose-invert max-w-none text-gray-300">
                <ReactMarkdown>{note}</ReactMarkdown>
            </div>
        </div>
    )
}
