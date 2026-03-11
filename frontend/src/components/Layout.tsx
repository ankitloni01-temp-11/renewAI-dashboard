import { Outlet } from 'react-router-dom'
import { useState } from 'react'
import Sidebar from './Sidebar'
import DemoControlPanel from './DemoControlPanel'
import WhatsAppSimulator from './WhatsAppSimulator'
import VoiceSimulator from './VoiceSimulator'
import GlobalIntelligencePipeline from './GlobalIntelligencePipeline'
import { useUIStore } from '../stores/uiStore'

export default function Layout() {
  const { whatsappOpen, voiceOpen } = useUIStore()

  return (
    <div className="flex h-screen bg-gray-100 overflow-hidden">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <DemoControlPanel />
        <main className="flex-1 overflow-auto p-4">
          <Outlet />
        </main>
      </div>
      {whatsappOpen && <WhatsAppSimulator />}
      {voiceOpen && <VoiceSimulator />}
      <GlobalIntelligencePipeline />
    </div>
  )
}
