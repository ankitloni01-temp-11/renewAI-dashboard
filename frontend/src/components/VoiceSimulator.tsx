import { useState, useRef, useEffect, useCallback } from 'react'
import { X, Mic, Phone, MicOff, Volume2 } from 'lucide-react'
import { useUIStore } from '../stores/uiStore'
import { useConversation } from '@elevenlabs/react'
import toast from 'react-hot-toast'

interface VoiceTurn { id: string; role: 'customer' | 'ai'; text: string; timestamp: Date }
const DEMO_POLICIES = [{ id: 'SLI-2298741', label: 'Rajesh Sharma' }, { id: 'SLI-882341', label: 'Meenakshi Iyer' }, { id: 'SLI-445678', label: 'Vikram Malhotra' }]

export default function VoiceSimulator() {
  const { setVoiceOpen, activeDemoPolicy } = useUIStore()
  const [turns, setTurns] = useState<VoiceTurn[]>([])
  const [policyId, setPolicyId] = useState(activeDemoPolicy || 'SLI-2298741')
  const [duration, setDuration] = useState(0)
  const bottomRef = useRef<HTMLDivElement>(null)

  const conversation = useConversation({
    onConnect: () => toast.success('Connected to ElevenLabs AI Agent'),
    onDisconnect: () => toast.error('Disconnected'),
    onMessage: (message: { message: string; source: 'user' | 'ai' }) => {
      setTurns(prev => [...prev, {
        id: Date.now().toString(),
        role: message.source === 'user' ? 'customer' : 'ai',
        text: message.message,
        timestamp: new Date()
      }])
    },
    onError: (error: string) => toast.error(`Error: ${error}`),
  })

  useEffect(() => {
    let t: any;
    if (conversation.status === 'connected') {
      t = setInterval(() => setDuration(d => d + 1), 1000);
    } else {
      setDuration(0);
    }
    return () => clearInterval(t)
  }, [conversation.status])

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [turns])

  const formatDuration = (s: number) => `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`

  const startCall = useCallback(async () => {
    try {
      await navigator.mediaDevices.getUserMedia({ audio: true })

      const agentId = import.meta.env.VITE_ELEVENLABS_AGENT_ID;
      if (!agentId) {
        toast.error("VITE_ELEVENLABS_AGENT_ID not configured in .env");
        return;
      }

      await (conversation as any).startSession({
        agentId: agentId as string,
      })
    } catch (error) {
      toast.error('Failed to start call. Please check microphone permissions.')
    }
  }, [conversation])

  const endCall = useCallback(async () => {
    await conversation.endSession()
  }, [conversation])

  const isConnected = conversation.status === 'connected'
  const isConnecting = conversation.status === 'connecting'

  return (
    <div className="fixed right-0 top-0 h-full w-96 bg-gray-900 shadow-2xl z-50 flex flex-col border-l border-gray-700">
      <div className="bg-gray-800 text-white p-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className={`w-8 h-8 ${isConnected ? 'bg-green-500 animate-pulse' : 'bg-gray-600'} rounded-full flex items-center justify-center`}>
            <Phone className="w-4 h-4 text-white" />
          </div>
          <div>
            <div className="font-semibold text-sm">ElevenLabs AI Voice Agent</div>
            <div className={`text-xs ${isConnected ? 'text-green-400' : 'text-gray-400'}`}>
              {isConnected ? `${formatDuration(duration)} • Active` : conversation.status}
            </div>
          </div>
        </div>
        <button onClick={() => { endCall(); setVoiceOpen(false) }} className="hover:bg-gray-700 rounded p-1"><X className="w-4 h-4 text-white" /></button>
      </div>

      <div className="bg-gray-800 px-3 py-2 border-b border-gray-700">
        <select value={policyId} onChange={e => { setPolicyId(e.target.value); setTurns([]) }}
          className="w-full text-xs bg-gray-700 text-white border border-gray-600 rounded px-2 py-1">
          {DEMO_POLICIES.map(p => <option key={p.id} value={p.id}>{p.label}</option>)}
        </select>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-900">
        {turns.length === 0 && (
          <div className="text-center text-gray-500 text-xs mt-8">
            <Mic className="w-8 h-8 mx-auto mb-2 opacity-30" />
            <p className="font-medium text-gray-400">Real-time Voice Conversation</p>
            <p className="mt-1 text-gray-500">The agent will speak in {policyId === 'SLI-2298741' ? 'Hindi' : 'English'}</p>
          </div>
        )}
        {turns.map(turn => (
          <div key={turn.id} className={`flex gap-2 ${turn.role === 'customer' ? 'flex-row-reverse' : ''}`}>
            <div className={`w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0 text-xs font-bold ${turn.role === 'ai' ? 'bg-blue-600 text-white' : 'bg-green-600 text-white'}`}>{turn.role === 'ai' ? 'AI' : 'C'}</div>
            <div className={`max-w-[80%] rounded-lg p-2.5 text-sm ${turn.role === 'ai' ? 'bg-gray-800 text-gray-100' : 'bg-green-900 text-green-100'}`}>
              <div className="text-xs font-semibold mb-1 opacity-60">{turn.role === 'ai' ? '▶ AI Agent' : '🎤 Customer'}</div>
              <p className="leading-relaxed">{turn.text}</p>
            </div>
          </div>
        ))}
        {conversation.isSpeaking && (
          <div className="flex gap-2">
            <div className="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center"><Volume2 className="w-3 h-3 text-white" /></div>
            <div className="bg-gray-800 rounded-lg p-2.5 flex items-center gap-2">
              <div className="flex gap-1">
                {[0, 1, 2].map((i: number) => <div key={i} className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: `${i * 0.15}s` }} />)}
              </div>
              <span className="text-[10px] text-gray-400 uppercase tracking-wider font-bold">Speaking</span>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="p-4 bg-gray-800 space-y-3">
        {!isConnected ? (
          <button
            onClick={startCall}
            disabled={isConnecting}
            className="w-full py-3 bg-green-600 hover:bg-green-500 disabled:bg-gray-600 rounded-xl flex items-center justify-center gap-2 font-bold text-white transition-all shadow-lg"
          >
            {isConnecting ? (
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <Mic className="w-5 h-5" />
            )}
            {isConnecting ? 'Connecting...' : 'Start Voice Call'}
          </button>
        ) : (
          <div className="space-y-3">
            <div className="flex items-center justify-center gap-4 py-2">
              <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full bg-gray-700 border ${conversation.isSpeaking ? 'border-blue-500' : 'border-gray-600'}`}>
                <div className={`w-2 h-2 rounded-full ${conversation.isSpeaking ? 'bg-blue-500 animate-pulse' : 'bg-gray-500'}`} />
                <span className="text-[10px] font-bold text-gray-300">AGENT</span>
              </div>
              <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full bg-gray-700 border ${!conversation.isSpeaking ? 'border-green-500' : 'border-gray-600'}`}>
                <div className={`w-2 h-2 rounded-full ${!conversation.isSpeaking ? 'bg-green-500 animate-pulse' : 'bg-gray-500'}`} />
                <span className="text-[10px] font-bold text-gray-300">YOU</span>
              </div>
            </div>
            <button
              onClick={endCall}
              className="w-full py-3 bg-red-600 hover:bg-red-500 rounded-xl flex items-center justify-center gap-2 font-bold text-white transition-all shadow-lg"
            >
              <MicOff className="w-5 h-5" />
              End Conversation
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
