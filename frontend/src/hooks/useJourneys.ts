import { useQuery, useQueryClient } from '@tanstack/react-query'
import api from '../api/client'
export const useJourneys = (status?: string) => {
  return useQuery({
    queryKey: ['journeys', status],
    queryFn: async () => {
      const { data } = await api.get('/api/journeys', { params: status ? { status_filter: status } : {} })
      return data
    },
    refetchInterval: 4000
  })
}
export const useJourney = (policyId: string) => {
  return useQuery({
    queryKey: ['journey', policyId],
    queryFn: async () => { const { data } = await api.get(`/api/journeys/${policyId}`); return data },
    refetchInterval: 3000,
    enabled: !!policyId
  })
}
