import { create } from 'zustand'

interface UIStore {
  sidebarOpen: boolean; whatsappOpen: boolean; voiceOpen: boolean
  selectedPolicyId: string; activeDemoPolicy: string
  setSidebarOpen: (v: boolean) => void; setWhatsappOpen: (v: boolean) => void
  setVoiceOpen: (v: boolean) => void; setSelectedPolicyId: (id: string) => void
  setActiveDemoPolicy: (id: string) => void
}

export const useUIStore = create<UIStore>((set) => ({
  sidebarOpen: true, whatsappOpen: false, voiceOpen: false,
  selectedPolicyId: 'SLI-2298741', activeDemoPolicy: 'SLI-2298741',
  setSidebarOpen: (v) => set({ sidebarOpen: v }),
  setWhatsappOpen: (v) => set({ whatsappOpen: v }),
  setVoiceOpen: (v) => set({ voiceOpen: v }),
  setSelectedPolicyId: (id) => set({ selectedPolicyId: id }),
  setActiveDemoPolicy: (id) => set({ activeDemoPolicy: id, selectedPolicyId: id })
}))
