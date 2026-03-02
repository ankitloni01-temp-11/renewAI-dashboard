import { useQuery } from '@tanstack/react-query'
import api from '../api/client'
export const useHumanQueue = (priority?: string, status?: string) => {
  return useQuery({
    queryKey: ['queue', priority, status],
    queryFn: async () => {
      const params: Record<string, string> = {}
      if (priority) params.priority = priority
      if (status) params.status = status
      const { data } = await api.get('/api/human-queue', { params })
      return data
    },
    refetchInterval: 4000
  })
}
export const useQueueCase = (caseId: string) => {
  return useQuery({
    queryKey: ['case', caseId],
    queryFn: async () => { const { data } = await api.get(`/api/human-queue/${caseId}`); return data },
    enabled: !!caseId
  })
}
