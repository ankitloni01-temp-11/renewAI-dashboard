import { useState } from 'react'
import { Play, MessageSquare, Phone, Zap } from 'lucide-react'
import toast from 'react-hot-toast'
import api from '../api/client'
import { useUIStore } from '../stores/uiStore'
import { useDashboardKPIs } from '../hooks/useKPIs'
import { useQueryClient } from '@tanstack/react-query'
import { formatINR } from '../utils/formatCurrency'

const DEMO_JOURNEYS = [
  { label: 'Rajesh (Happy Path)', policyId: 'SLI-2298741', color: 'bg-green-600 hover:bg-green-700' },
  { label: 'Meenakshi (Distress)', policyId: 'SLI-8872134', color: 'bg-red-600 hover:bg-red-700' },
  { label: 'Vikram (Email-only)', policyId: 'SLI-5567123', color: 'bg-purple-600 hover:bg-purple-700' },
]

export default function DemoControlPanel() {
  const [scanCount, setScanCount] = useState(5)
  const [scanning, setScanning] = useState(false)
  const { setWhatsappOpen, setVoiceOpen, setActiveDemoPolicy, setGlobalTriggerPolicy, whatsappOpen, voiceOpen } = useUIStore()
  const { data: kpis } = useDashboardKPIs()
  const queryClient = useQueryClient()

  const runScan = async () => {
    setScanning(true)
    try {
      const { data } = await api.post(`/api/triggers/t45-scan?count=${scanCount}`)
      toast.success(`🚀 Started ${data.triggered} renewal journeys!`)
      queryClient.invalidateQueries({ queryKey: ['journeys'] })
    } catch {
      toast.error('Scan failed - is backend running?')
    } finally {
      setScanning(false)
    }
  }

  const runDemoJourney = async (policyId: string, label: string) => {
    try {
      // 1. Trigger the backend
      await api.post(`/api/triggers/single/${policyId}`)

      // 2. Fetch full policy details for the modal
      const { data: pol } = await api.get(`/api/policies/${policyId}`)

      // 3. Open the global pipeline modal
      setGlobalTriggerPolicy(pol)

      setActiveDemoPolicy(policyId)
      queryClient.invalidateQueries({ queryKey: ['journeys'] })
    } catch {
      toast.error('Failed to start journey')
    }
  }

  const sb = kpis?.status_bar || {}

  return (
    <div className="bg-gray-900 text-white px-3 py-2 flex items-center gap-2 flex-wrap text-xs border-b border-gray-700">
      {/* T-45 Scan */}
      <div className="flex items-center gap-1">
        <select value={scanCount} onChange={e => setScanCount(Number(e.target.value))} className="bg-gray-700 text-white rounded px-1.5 py-1 text-xs">
          {[1, 5, 10, 25].map(n => <option key={n} value={n}>{n}</option>)}
        </select>
        <button onClick={runScan} disabled={scanning} className="flex items-center gap-1 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 px-2 py-1 rounded transition-all">
          <Zap className="w-3 h-3" />{scanning ? 'Running...' : 'T-45 Scan'}
        </button>
      </div>

      <div className="w-px h-4 bg-gray-600" />

      {/* Demo journeys */}
      {DEMO_JOURNEYS.map(j => (
        <button key={j.policyId} onClick={() => runDemoJourney(j.policyId, j.label)}
          className={`flex items-center gap-1 px-2 py-1 rounded transition-all text-white ${j.color}`}>
          <Play className="w-3 h-3" />{j.label}
        </button>
      ))}

      <div className="w-px h-4 bg-gray-600" />

      {/* Simulators */}
      <button onClick={() => setWhatsappOpen(!whatsappOpen)}
        className={`flex items-center gap-1 px-2 py-1 rounded transition-all ${whatsappOpen ? 'bg-green-700' : 'bg-green-600 hover:bg-green-700'}`}>
        <MessageSquare className="w-3 h-3" />WhatsApp Sim
      </button>
      <button onClick={() => setVoiceOpen(!voiceOpen)}
        className={`flex items-center gap-1 px-2 py-1 rounded transition-all ${voiceOpen ? 'bg-indigo-700' : 'bg-indigo-600 hover:bg-indigo-700'}`}>
        <Phone className="w-3 h-3" />Voice Sim
      </button>

      {/* Live stats from real data */}
      <div className="ml-auto flex items-center gap-3 text-gray-300">
        <span className="flex items-center gap-1">
          <span className="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse" />
          Active: <b className="text-white ml-1">{sb.active ?? 0}</b>
        </span>
        <span>Paid: <b className="text-green-400">{sb.paid ?? 0}</b></span>
        <span>Escalated: <b className="text-red-400">{sb.escalated ?? 0}</b></span>
        <span>Today: <b className="text-yellow-400">{formatINR(sb.today_premium ?? 0)}</b></span>
      </div>
    </div>
  )
}
