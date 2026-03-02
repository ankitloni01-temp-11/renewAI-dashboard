import { useState } from 'react'
import { Shield } from 'lucide-react'
import { useAuthStore } from '../stores/authStore'
import { ROLES } from '../utils/roleConfig'
import { UserRole } from '../types'

export default function LoginPage() {
  const [selectedRole, setSelectedRole] = useState<UserRole>('renewal_head')
  const { setUser } = useAuthStore()

  const login = () => {
    const roleInfo = ROLES.find(r => r.id === selectedRole)!
    setUser({ id: selectedRole, name: roleInfo.name.split('(')[0].trim(), role: selectedRole })
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#1B4F8A] to-[#0d2d52] flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md">
        <div className="flex items-center justify-center gap-3 mb-6">
          <Shield className="w-10 h-10 text-[#1B4F8A]" />
          <div>
            <h1 className="text-2xl font-bold text-[#1B4F8A]">RenewAI</h1>
            <p className="text-sm text-gray-500">Suraksha Life Insurance</p>
          </div>
        </div>
        <div className="bg-blue-50 rounded-xl p-4 mb-6 text-sm text-blue-800">
          <strong>Project RenewAI Demo</strong> — 4.8M policyholders, 6-agent AI system, Team of 20
        </div>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Demo as:</label>
            <div className="space-y-2">
              {ROLES.map(role => (
                <label key={role.id} className={`flex items-center gap-3 p-3 rounded-lg border-2 cursor-pointer transition-all ${selectedRole === role.id ? 'border-[#1B4F8A] bg-blue-50' : 'border-gray-200 hover:border-gray-300'}`}>
                  <input type="radio" name="role" value={role.id} checked={selectedRole === role.id}
                    onChange={() => setSelectedRole(role.id as UserRole)} className="text-[#1B4F8A]" />
                  <span className="text-sm font-medium text-gray-800">{role.name}</span>
                </label>
              ))}
            </div>
          </div>
          <button onClick={login}
            className="w-full bg-[#1B4F8A] hover:bg-[#154070] text-white font-semibold py-3 rounded-xl transition-all shadow-md">
            Enter Dashboard →
          </button>
        </div>
        <p className="text-center text-xs text-gray-400 mt-4">Demo build — No real data or payments</p>
      </div>
    </div>
  )
}
