import ChannelIcon from './ChannelIcon'
import CritiqueBadge from './CritiqueBadge'
import type { Message } from '../types'
import { formatDate } from '../utils/formatDate'

interface ConversationTimelineProps {
    messages: Message[]
}

export default function ConversationTimeline({ messages }: ConversationTimelineProps) {
    if (!messages || messages.length === 0) {
        return <div className="text-gray-500 text-sm py-4 text-center">No conversation history yet.</div>
    }

    return (
        <div className="bg-gray-800/60 rounded-xl p-5 border border-gray-700">
            <h3 className="text-lg font-semibold text-white mb-4">Conversation Timeline</h3>
            <div className="space-y-3">
                {messages.map((msg, i) => (
                    <div key={msg.message_id || i} className={`flex gap-3 ${msg.role === 'customer' ? 'flex-row-reverse' : ''}`}>
                        <div className="flex-shrink-0 mt-1">
                            <ChannelIcon channel={msg.channel} size={18} />
                        </div>
                        <div className={`flex-1 max-w-[80%] ${msg.role === 'customer' ? 'text-right' : ''}`}>
                            <div className={`inline-block rounded-xl px-4 py-2.5 text-sm ${msg.role === 'customer'
                                    ? 'bg-emerald-900/40 text-emerald-100 rounded-tr-sm'
                                    : 'bg-gray-700/60 text-gray-200 rounded-tl-sm'
                                }`}>
                                {msg.role === 'customer' ? msg.customer_text : msg.ai_response}
                            </div>
                            <div className="flex items-center gap-2 mt-1 text-xs text-gray-500">
                                <span>{formatDate(msg.timestamp)}</span>
                                {msg.detected_intent && <span className="px-1.5 py-0.5 bg-gray-700 rounded text-gray-400">{msg.detected_intent}</span>}
                                {msg.critique_score !== undefined && <CritiqueBadge score={msg.critique_score} />}
                                {msg.safety_verdict && msg.safety_verdict !== 'PASS' && (
                                    <span className="px-1.5 py-0.5 bg-red-900/50 rounded text-red-300">⚠ {msg.safety_verdict}</span>
                                )}
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}
