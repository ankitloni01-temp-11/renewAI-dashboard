import { useState, useRef, useEffect } from 'react'
import { X, Mic, Phone } from 'lucide-react'
import { useUIStore } from '../stores/uiStore'
import api from '../api/client'
import toast from 'react-hot-toast'

interface VoiceTurn { id: string; role: 'customer'|'ai'; text: string; intent?: string; critique?: number; timestamp: Date }
const QUICK_RESPONSES = ['Haan, payment karna hai','Nahi, baad mein','Paise nahi hain','Kisi insaan se baat karo','Policy band karo','EMI mein ho sakta hai?','Mujhe already pay kiya hai','What is my sum assured?']
const DEMO_POLICIES = [{ id: 'SLI-2298741', label: 'Rajesh Sharma' },{ id: 'SLI-882341', label: 'Meenakshi Iyer' },{ id: 'SLI-445678', label: 'Vikram Malhotra' }]

export default function VoiceSimulator() {
  const { setVoiceOpen, activeDemoPolicy } = useUIStore()
  const [turns, setTurns] = useState<VoiceTurn[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [policyId, setPolicyId] = useState(activeDemoPolicy || 'SLI-2298741')
  const [callId] = useState(`call_demo_${Date.now()}`)
  const [duration, setDuration] = useState(0)
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => { const t = setInterval(() => setDuration(d => d+1), 1000); return () => clearInterval(t) }, [])
  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [turns])

  const formatDuration = (s: number) => `${String(Math.floor(s/60)).padStart(2,'0')}:${String(s%60).padStart(2,'0')}`

  const sendTurn = async (text: string) => {
    if (!text.trim() || loading) return
    setTurns(prev => [...prev, { id: Date.now().toString(), role: 'customer', text, timestamp: new Date() }])
    setInput(''); setLoading(true)
    try {
      const { data } = await api.post('/api/conversations/voice/turn', null, { params: { policy_id: policyId, call_id: callId, customer_text: text } })
      setTurns(prev => [...prev, { id: (Date.now()+1).toString(), role: 'ai', text: data.ai_response || '...', intent: data.detected_intent, critique: data.critique_score, timestamp: new Date() }])
      if (data.escalated) toast.error(`🚨 Escalated to human! Case: ${data.case_id}`, { duration: 5000 })
    } catch {
      setTurns(prev => [...prev, { id: Date.now().toString(), role: 'ai', text: '⚠️ Backend not connected.', timestamp: new Date() }])
    } finally { setLoading(false) }
  }

  return (
    <div className="fixed right-0 top-0 h-full w-96 bg-gray-900 shadow-2xl z-50 flex flex-col border-l border-gray-700">
      <div className="bg-gray-800 text-white p-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center animate-pulse"><Phone className="w-4 h-4 text-white" /></div>
          <div><div className="font-semibold text-sm">AI Voice Call</div><div className="text-xs text-green-400">{formatDuration(duration)} • Active</div></div>
        </div>
        <button onClick={() => setVoiceOpen(false)} className="hover:bg-gray-700 rounded p-1"><X className="w-4 h-4 text-white" /></button>
      </div>
      <div className="bg-gray-800 px-3 py-2 border-b border-gray-700">
        <select value={policyId} onChange={e => { setPolicyId(e.target.value); setTurns([]) }}
          className="w-full text-xs bg-gray-700 text-white border border-gray-600 rounded px-2 py-1">
          {DEMO_POLICIES.map(p => <option key={p.id} value={p.id}>{p.label}</option>)}
        </select>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-900">
        {turns.length === 0 && <div className="text-center text-gray-500 text-xs mt-8"><Mic className="w-8 h-8 mx-auto mb-2 opacity-30" /><p>Simulating an AI voice call</p><p className="mt-1 text-gray-600">Type what the customer says</p></div>}
        {turns.map(turn => (
          <div key={turn.id} className={`flex gap-2 ${turn.role === 'customer' ? 'flex-row-reverse' : ''}`}>
            <div className={`w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0 text-xs font-bold ${turn.role === 'ai' ? 'bg-blue-600 text-white' : 'bg-green-600 text-white'}`}>{turn.role === 'ai' ? 'AI' : 'C'}</div>
            <div className={`max-w-[80%] rounded-lg p-2.5 text-sm ${turn.role === 'ai' ? 'bg-gray-800 text-gray-100' : 'bg-green-900 text-green-100'}`}>
              <div className="text-xs font-semibold mb-1 opacity-60">{turn.role === 'ai' ? '▶ AI Agent' : '🎤 Customer'}</div>
              <p className="leading-relaxed">{turn.text}</p>
              {turn.intent && <div className="mt-1 text-xs text-gray-400">Intent: {turn.intent}</div>}
              {turn.critique && <div className="text-xs text-blue-400 mt-0.5">Critique: {turn.critique.toFixed(1)}/10</div>}
            </div>
          </div>
        ))}
        {loading && <div className="flex gap-2"><div className="w-6 h-6 bg-blue-600 rounded-full" /><div className="bg-gray-800 rounded-lg p-2.5 flex gap-1">{[0,1,2].map(i => <div key={i} className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: `${i*0.15}s` }} />)}</div></div>}
        <div ref={bottomRef} />
      </div>
      <div className="px-3 py-2 bg-gray-800 border-t border-gray-700 flex gap-1 overflow-x-auto">
        {QUICK_RESPONSES.map(q => <button key={q} onClick={() => sendTurn(q)} className="flex-shrink-0 text-xs bg-gray-700 hover:bg-gray-600 text-gray-300 px-2 py-1 rounded-full transition-all">{q.length > 20 ? q.slice(0,20)+'…' : q}</button>)}
      </div>
      <div className="p-3 bg-gray-800 flex gap-2">
        <input value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key==='Enter' && sendTurn(input)} placeholder="Type what the customer says..." disabled={loading}
          className="flex-1 rounded-full px-4 py-2 text-sm bg-gray-700 text-white border border-gray-600 outline-none placeholder-gray-500" />
        <button onClick={() => sendTurn(input)} disabled={loading || !input.trim()}
          className="w-10 h-10 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 rounded-full flex items-center justify-center transition-all">
          <Mic className="w-4 h-4 text-white" />
        </button>
      </div>
    </div>
  )
}
