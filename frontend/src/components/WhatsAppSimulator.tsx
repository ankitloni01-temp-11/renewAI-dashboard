import { useState, useRef, useEffect } from 'react'
import { X, Send, MessageSquare } from 'lucide-react'
import { useUIStore } from '../stores/uiStore'
import api from '../api/client'
import toast from 'react-hot-toast'

interface ChatMsg {
  id: string; role: 'customer' | 'ai'; text: string
  intent?: string; critique?: number; safety?: string
  timestamp: Date; escalated?: boolean
}

const QUICK_MESSAGES = [
  'Can I pay in two instalments?', 'Too expensive for me',
  'My husband passed away last month', 'I want to talk to a person',
  'I already paid', 'What is my sum assured?', 'Can I pay via UPI?', 'I want to cancel',
]
const DEMO_POLICIES = [
  { id: 'SLI-2298741', label: 'Rajesh Sharma - Term Shield' },
  { id: 'SLI-882341', label: 'Meenakshi Iyer - Endowment Plus' },
  { id: 'SLI-445678', label: 'Vikram Malhotra - ULIP' },
]

export default function WhatsAppSimulator() {
  const { setWhatsappOpen, activeDemoPolicy } = useUIStore()
  const [messages, setMessages] = useState<ChatMsg[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [policyId, setPolicyId] = useState(activeDemoPolicy || 'SLI-2298741')
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [messages])

  const sendMessage = async (text: string) => {
    if (!text.trim() || loading) return
    setMessages(prev => [...prev, { id: Date.now().toString(), role: 'customer', text, timestamp: new Date() }])
    setInput('')
    setLoading(true)
    try {
      const { data } = await api.post('/api/conversations/whatsapp/message', null, {
        params: { policy_id: policyId, customer_message: text }
      })
      setMessages(prev => [...prev, {
        id: (Date.now()+1).toString(), role: 'ai',
        text: data.ai_response || 'Processing...', intent: data.detected_intent,
        critique: data.critique_score, safety: data.safety_verdict,
        timestamp: new Date(), escalated: data.escalated
      }])
      if (data.escalated) toast.error(`🚨 DISTRESS DETECTED - Escalated! Case: ${data.case_id}`, { duration: 6000 })
    } catch {
      setMessages(prev => [...prev, { id: Date.now().toString(), role: 'ai', text: '⚠️ Backend not connected. Add GOOGLE_API_KEY and start backend.', timestamp: new Date() }])
    } finally { setLoading(false) }
  }

  return (
    <div className="fixed right-0 top-0 h-full w-96 bg-white shadow-2xl z-50 flex flex-col border-l border-gray-200">
      <div className="bg-[#075E54] text-white p-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-green-400 rounded-full flex items-center justify-center"><MessageSquare className="w-4 h-4 text-white" /></div>
          <div><div className="font-semibold text-sm">Suraksha RenewAI</div><div className="text-xs text-green-300">AI-powered renewal assistant</div></div>
        </div>
        <button onClick={() => setWhatsappOpen(false)} className="hover:bg-green-700 rounded p-1"><X className="w-4 h-4" /></button>
      </div>
      <div className="bg-[#ECE5DD] px-3 py-2 border-b">
        <select value={policyId} onChange={e => { setPolicyId(e.target.value); setMessages([]) }}
          className="w-full text-xs bg-white border border-gray-300 rounded px-2 py-1">
          {DEMO_POLICIES.map(p => <option key={p.id} value={p.id}>{p.label}</option>)}
        </select>
      </div>
      <div className="flex-1 overflow-y-auto p-3 space-y-3 bg-[#ECE5DD]">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 text-xs mt-8">
            <MessageSquare className="w-8 h-8 mx-auto mb-2 opacity-30" />
            <p>Start a conversation as the customer</p><p className="mt-1 text-gray-400">Real AI will respond!</p>
          </div>
        )}
        {messages.map(msg => (
          <div key={msg.id} className={`flex ${msg.role === 'customer' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] rounded-lg p-2.5 shadow-sm text-sm ${msg.role === 'customer' ? 'bg-[#DCF8C6]' : msg.escalated ? 'bg-red-100 border border-red-300' : 'bg-white'} text-gray-800`}>
              {msg.escalated && <div className="text-red-600 font-bold text-xs mb-1">🚨 DISTRESS DETECTED - Escalated to Human Queue</div>}
              <p className="whitespace-pre-wrap leading-relaxed">{msg.text}</p>
              <div className="flex items-center justify-between mt-1 gap-2">
                <span className="text-xs text-gray-400">{msg.timestamp.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' })}</span>
                {msg.role === 'ai' && msg.critique && <span className="text-xs bg-blue-100 text-blue-700 px-1 rounded">Critique: {msg.critique.toFixed(1)}/10</span>}
                {msg.role === 'ai' && msg.intent && <span className="text-xs bg-gray-100 text-gray-600 px-1 rounded">{msg.intent}</span>}
              </div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white rounded-lg p-3 shadow-sm flex gap-1">
              {[0,1,2].map(i => <div key={i} className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: `${i*0.15}s` }} />)}
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>
      <div className="px-3 py-2 bg-white border-t flex gap-1 overflow-x-auto">
        {QUICK_MESSAGES.map(q => (
          <button key={q} onClick={() => sendMessage(q)}
            className="flex-shrink-0 text-xs bg-gray-100 hover:bg-green-100 text-gray-700 px-2 py-1 rounded-full border transition-all">
            {q.length > 18 ? q.slice(0, 18) + '…' : q}
          </button>
        ))}
      </div>
      <div className="p-3 bg-[#F0F0F0] flex gap-2">
        <input value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && sendMessage(input)}
          placeholder="Type a message as the customer..." disabled={loading}
          className="flex-1 rounded-full px-4 py-2 text-sm border-none outline-none bg-white shadow-sm" />
        <button onClick={() => sendMessage(input)} disabled={loading || !input.trim()}
          className="w-10 h-10 bg-[#25D366] hover:bg-[#20c15e] disabled:opacity-50 rounded-full flex items-center justify-center shadow-sm transition-all">
          <Send className="w-4 h-4 text-white" />
        </button>
      </div>
    </div>
  )
}
