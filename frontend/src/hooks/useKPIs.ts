import { useQuery } from '@tanstack/react-query'
import api from '../api/client'
export const useKPIs = () => {
  return useQuery({
    queryKey: ['kpis'],
    queryFn: async () => { const { data } = await api.get('/api/kpis'); return data },
    refetchInterval: 5000
  })
}
export const useFinancial = () => {
  return useQuery({
    queryKey: ['kpis-financial'],
    queryFn: async () => { const { data } = await api.get('/api/kpis/financial'); return data }
  })
}
