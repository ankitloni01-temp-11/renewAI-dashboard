import { useQuery } from '@tanstack/react-query'
import api from '../api/client'
export const useConversationHistory = (policyId: string) => {
  return useQuery({
    queryKey: ['conversation', policyId],
    queryFn: async () => { const { data } = await api.get(`/api/conversations/${policyId}/history`); return data },
    enabled: !!policyId, refetchInterval: 2000
  })
}
