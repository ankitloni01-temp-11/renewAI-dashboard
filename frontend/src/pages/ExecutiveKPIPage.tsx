import { useKPIs, useFinancial } from '../hooks/useKPIs'
import { TrendingUp, TrendingDown, Target, AlertCircle, CheckCircle, DollarSign } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line, CartesianGrid, PieChart, Pie, Cell } from 'recharts'
import { formatINR, formatCrore } from '../utils/formatCurrency'

const KPI_DEFS = [
  { key: 'persistency_rate', label: '13th Month Persistency', baseline: 71, target: 88, unit: '%', good: 'high' },
  { key: 'cost_per_renewal', label: 'Cost per Renewal', baseline: 182, target: 45, unit: '₹', good: 'low' },
  { key: 'email_open_rate', label: 'Email Open Rate', baseline: 18, target: 42, unit: '%', good: 'high' },
  { key: 'whatsapp_response_rate', label: 'WhatsApp Response Rate', baseline: 0, target: 58, unit: '%', good: 'high' },
  { key: 'voice_conversion_rate', label: 'Voice Call Conversion', baseline: 0, target: 31, unit: '%', good: 'high' },
  { key: 'human_escalation_rate', label: 'Human Escalation Rate', baseline: 100, target: 10, unit: '%', good: 'low' },
  { key: 'customer_nps', label: 'Customer NPS', baseline: 34, target: 55, unit: '', good: 'high' },
  { key: 'irdai_violations', label: 'IRDAI Violations', baseline: 12, target: 0, unit: '/yr', good: 'low' },
  { key: 'ai_accuracy_score', label: 'AI Response Accuracy', baseline: 0, target: 87, unit: '%', good: 'high' },
  { key: 'distress_escalation_pct', label: 'Distress Escalated <2h', baseline: 0, target: 100, unit: '%', good: 'high' },
]

function KPICard({ kpiDef, value }: { kpiDef: typeof KPI_DEFS[0]; value: number }) {
  const isGood = kpiDef.good === 'high' ? value >= kpiDef.target : value <= kpiDef.target
  const pct = kpiDef.good === 'high'
    ? Math.min(100, ((value - kpiDef.baseline) / (kpiDef.target - kpiDef.baseline)) * 100)
    : Math.min(100, ((kpiDef.baseline - value) / (kpiDef.baseline - kpiDef.target)) * 100)

  return (
    <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
      <div className="flex items-start justify-between mb-2">
        <p className="text-xs text-gray-500 font-medium leading-tight">{kpiDef.label}</p>
        {isGood ? <CheckCircle className="w-4 h-4 text-green-500 flex-shrink-0" /> : <AlertCircle className="w-4 h-4 text-yellow-500 flex-shrink-0" />}
      </div>
      <div className="flex items-end gap-2 mb-2">
        <span className="text-2xl font-bold text-gray-900">{kpiDef.unit === '₹' ? kpiDef.unit : ''}{value.toFixed(kpiDef.unit === '₹' ? 0 : 1)}{kpiDef.unit !== '₹' ? kpiDef.unit : ''}</span>
        <span className={`text-xs font-medium mb-1 ${isGood ? 'text-green-600' : 'text-yellow-600'}`}>
          Target: {kpiDef.unit === '₹' ? kpiDef.unit : ''}{kpiDef.target}{kpiDef.unit !== '₹' ? kpiDef.unit : ''}
        </span>
      </div>
      <div className="w-full bg-gray-100 rounded-full h-1.5">
        <div className={`h-1.5 rounded-full transition-all ${isGood ? 'bg-green-500' : 'bg-yellow-400'}`}
          style={{ width: `${Math.max(0, pct)}%` }} />
      </div>
      <p className="text-xs text-gray-400 mt-1">Baseline: {kpiDef.unit === '₹' ? kpiDef.unit : ''}{kpiDef.baseline}{kpiDef.unit !== '₹' ? kpiDef.unit : ''}</p>
    </div>
  )
}

const FUNNEL_DATA = [
  { name: 'Total Policies', value: 14400, fill: '#1B4F8A' },
  { name: 'Email Sent', value: 12800, fill: '#2563EB' },
  { name: 'WA Sent', value: 8400, fill: '#16A34A' },
  { name: 'Voice Calls', value: 3200, fill: '#9333EA' },
  { name: 'Payments', value: 12672, fill: '#D97706' },
]

export default function ExecutiveKPIPage() {
  const { data: kpis, isLoading } = useKPIs()
  const { data: financial } = useFinancial()

  if (isLoading) return <div className="flex items-center justify-center h-64 text-gray-500">Loading KPIs...</div>

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Executive KPI Dashboard</h1>
          <p className="text-sm text-gray-500 mt-1">Project RenewAI — FY2025-26 | Suraksha Life Insurance</p>
        </div>
        <div className="flex gap-4">
          {[
            { label: '3-Yr NPV', value: '₹89 Cr', color: 'text-green-700' },
            { label: 'Payback', value: '7.8 Mo', color: 'text-blue-700' },
            { label: 'Team', value: '20 People', color: 'text-purple-700' },
          ].map(m => (
            <div key={m.label} className="bg-white rounded-xl p-3 shadow-sm border text-center">
              <div className={`text-xl font-bold ${m.color}`}>{m.value}</div>
              <div className="text-xs text-gray-500">{m.label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* 10 KPIs */}
      <div>
        <h2 className="text-sm font-semibold text-gray-600 uppercase tracking-wide mb-3">10 Success KPIs</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
          {KPI_DEFS.map(kd => <KPICard key={kd.key} kpiDef={kd} value={kpis?.[kd.key as keyof typeof kpis] as number ?? 0} />)}
        </div>
      </div>

      {/* Financial + Channel */}
      <div className="grid grid-cols-2 gap-6">
        <div className="bg-white rounded-xl p-4 shadow-sm border">
          <h3 className="font-semibold text-gray-800 mb-4">Financial Performance (₹ Crore)</h3>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={[
              { month: 'Jan', saving: 1.075, revenue: 3.24 },
              { month: 'Feb', saving: 1.075, revenue: 3.24 },
              { month: 'Mar', saving: 1.075, revenue: 3.24 },
            ]}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="month" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip formatter={(v: number) => `₹${v.toFixed(2)} Cr`} />
              <Bar dataKey="saving" name="Cost Saving" fill="#1B4F8A" radius={[4,4,0,0]} />
              <Bar dataKey="revenue" name="Revenue Uplift" fill="#D4860B" radius={[4,4,0,0]} />
            </BarChart>
          </ResponsiveContainer>
          <div className="grid grid-cols-3 gap-2 mt-3">
            {[
              { label: 'Annual Saving', value: '₹12.9 Cr', color: 'bg-blue-50 text-blue-800' },
              { label: 'Revenue Uplift', value: '₹38.9 Cr', color: 'bg-yellow-50 text-yellow-800' },
              { label: 'Net Year 1', value: '₹48 Cr', color: 'bg-green-50 text-green-800' },
            ].map(m => (
              <div key={m.label} className={`rounded-lg p-2 text-center ${m.color}`}>
                <div className="text-sm font-bold">{m.value}</div>
                <div className="text-xs">{m.label}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-xl p-4 shadow-sm border">
          <h3 className="font-semibold text-gray-800 mb-4">Journey Funnel (Monthly)</h3>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={FUNNEL_DATA} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis type="number" tick={{ fontSize: 10 }} />
              <YAxis dataKey="name" type="category" tick={{ fontSize: 10 }} width={80} />
              <Tooltip formatter={(v: number) => v.toLocaleString('en-IN')} />
              <Bar dataKey="value" radius={[0,4,4,0]}>
                {FUNNEL_DATA.map((entry, i) => <Cell key={i} fill={entry.fill} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* System Stats */}
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: 'Total Journeys', value: kpis?.total_journeys ?? 0, color: 'bg-blue-600' },
          { label: 'Payments Completed', value: kpis?.paid_journeys ?? 0, color: 'bg-green-600' },
          { label: 'Active Now', value: kpis?.active_journeys ?? 0, color: 'bg-yellow-500' },
          { label: 'Escalated', value: kpis?.escalated_journeys ?? 0, color: 'bg-red-500' },
        ].map(s => (
          <div key={s.label} className="bg-white rounded-xl p-4 shadow-sm border flex items-center gap-3">
            <div className={`w-3 h-10 rounded-full ${s.color}`} />
            <div>
              <div className="text-2xl font-bold text-gray-900">{s.value.toLocaleString()}</div>
              <div className="text-xs text-gray-500">{s.label}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
