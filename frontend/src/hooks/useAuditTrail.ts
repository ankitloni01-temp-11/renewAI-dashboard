import { useQuery } from '@tanstack/react-query'
import api from '../api/client'
export const useAuditTrail = (policyId: string) => {
  return useQuery({
    queryKey: ['audit', policyId],
    queryFn: async () => { const { data } = await api.get(`/api/audit/${policyId}`); return data },
    enabled: !!policyId, refetchInterval: 3000
  })
}
