import { useQuery } from '@tanstack/react-query'
import axios from '../api/client'
import { formatCurrency } from '../utils/formatCurrency'
import { formatDate } from '../utils/formatDate'

export default function RevivalPage() {
    const { data: journeyData } = useQuery({
        queryKey: ['journeys', 'lapsed'],
        queryFn: () => axios.get('/api/journeys?status=lapsed').then(r => r.data),
        refetchInterval: 10000,
    })

    const lapsedJourneys = journeyData?.journeys || []

    return (
        <div className="p-6 space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-white">Revival Cases</h1>
                    <p className="text-gray-400 text-sm mt-1">Lapsed policies eligible for revival campaigns</p>
                </div>
                <div className="flex items-center gap-3">
                    <span className="text-sm text-gray-400">{lapsedJourneys.length} lapsed policies</span>
                </div>
            </div>

            {lapsedJourneys.length === 0 ? (
                <div className="bg-gray-800/60 rounded-xl p-12 text-center border border-gray-700">
                    <p className="text-gray-400 text-lg">No lapsed policies currently.</p>
                    <p className="text-gray-500 text-sm mt-2">Policies that lapse after the full T-45 journey will appear here for revival.</p>
                </div>
            ) : (
                <div className="grid gap-4">
                    {lapsedJourneys.map((j: Record<string, unknown>) => (
                        <div key={j.policy_id as string} className="bg-gray-800/60 rounded-xl p-5 border border-gray-700 hover:border-gray-600 transition-colors">
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-4">
                                    <div className="w-10 h-10 rounded-full bg-red-900/40 flex items-center justify-center text-red-400 font-bold text-sm">
                                        LP
                                    </div>
                                    <div>
                                        <h3 className="text-white font-medium">{j.policy_id as string}</h3>
                                        <p className="text-gray-400 text-xs">
                                            Customer: {j.customer_id as string || 'Unknown'} •
                                            Lapsed: {j.paid_at ? formatDate(j.paid_at as string) : 'N/A'}
                                        </p>
                                    </div>
                                </div>
                                <div className="flex items-center gap-3">
                                    <span className="text-red-400 text-sm font-medium">LAPSED</span>
                                    <button className="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white text-sm rounded-lg transition-colors">
                                        Start Revival
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}
