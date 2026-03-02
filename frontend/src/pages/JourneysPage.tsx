import { useJourneys } from '../hooks/useJourneys'
import { useEffect, useState } from 'react'
import { formatINR } from '../utils/formatCurrency'
import { timeAgo } from '../utils/formatDate'
import { useUIStore } from '../stores/uiStore'


const STATUS_COLORS: Record<string, string> = {
  paid: 'bg-green-100 text-green-700', email_sent: 'bg-blue-100 text-blue-700',
  whatsapp_sent: 'bg-green-100 text-green-600', voice_scheduled: 'bg-purple-100 text-purple-700',
  planning: 'bg-yellow-100 text-yellow-700', escalated: 'bg-red-100 text-red-700',
  not_started: 'bg-gray-100 text-gray-500', error: 'bg-red-200 text-red-800', lapsed: 'bg-gray-200 text-gray-600'
}

export default function JourneysPage() {
  const [statusFilter, setStatusFilter] = useState('')
  const { data, isLoading } = useJourneys(statusFilter || undefined)
  const journeys = data?.journeys || []

  const counts = journeys.reduce((acc: Record<string, number>, j: Record<string, string>) => {
    acc[j.status] = (acc[j.status] || 0) + 1; return acc
  }, {} as Record<string, number>)

  return (
    <div className="space-y-4">
      <div><h1 className="text-2xl font-bold text-gray-900">Renewal Journeys</h1><p className="text-sm text-gray-500">{journeys.length} journeys • Live updates every 4s</p></div>
      
      <div className="flex gap-2 flex-wrap">
        <button onClick={() => setStatusFilter('')} className={`px-3 py-1.5 rounded-lg text-sm ${!statusFilter ? 'bg-[#1B4F8A] text-white' : 'bg-white border text-gray-600 hover:border-blue-300'}`}>All ({data?.total || 0})</button>
        {Object.entries(counts).map(([status, count]) => (
          <button key={status} onClick={() => setStatusFilter(status)}
            className={`px-3 py-1.5 rounded-lg text-sm ${statusFilter === status ? 'bg-[#1B4F8A] text-white' : 'bg-white border text-gray-600 hover:border-blue-300'}`}>
            {status} ({count as number})
          </button>
        ))}
      </div>

      {isLoading ? <div className="text-center py-8 text-gray-400">Loading journeys...</div> : (
        <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 border-b">
              <tr>{['Policy ID','Status','Current Step','Channel','Language','Started','Updated','Payment'].map(h => <th key={h} className="text-left px-3 py-2 text-xs font-semibold text-gray-500">{h}</th>)}</tr>
            </thead>
            <tbody>
              {journeys.slice(0,50).map((j: Record<string, string | number | null>) => (
                <tr key={String(j.policy_id)} className="border-b hover:bg-gray-50">
                  <td className="px-3 py-2 font-medium text-blue-700">{String(j.policy_id)}</td>
                  <td className="px-3 py-2"><span className={`px-2 py-0.5 rounded text-xs font-medium ${STATUS_COLORS[String(j.status)] || 'bg-gray-100 text-gray-600'}`}>{String(j.status)}</span></td>
                  <td className="px-3 py-2 text-gray-500 text-xs">{j.current_step ? String(j.current_step) : '-'}</td>
                  <td className="px-3 py-2 text-xs capitalize">{j.channel ? String(j.channel) : '-'}</td>
                  <td className="px-3 py-2 text-xs">{j.language ? String(j.language) : '-'}</td>
                  <td className="px-3 py-2 text-xs text-gray-400">{j.started_at ? timeAgo(String(j.started_at)) : '-'}</td>
                  <td className="px-3 py-2 text-xs text-gray-400">{j.updated_at ? timeAgo(String(j.updated_at)) : '-'}</td>
                  <td className="px-3 py-2 text-xs font-medium text-green-700">{j.payment_amount ? formatINR(Number(j.payment_amount)) : '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
