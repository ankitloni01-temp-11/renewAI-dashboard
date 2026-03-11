import { useKPIs, useFinancial, useFunnel } from '../hooks/useKPIs'
import { TrendingUp, TrendingDown, Target, AlertCircle, CheckCircle, Clock } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell } from 'recharts'

const KPI_DEFS = [
  { key: 'persistency_rate', label: '13th Month Persistency', baseline: 71, target: 88, unit: '%', good: 'high' },
  { key: 'cost_per_renewal', label: 'Cost per Renewal', baseline: 182, target: 45, unit: '₹', good: 'low' },
  { key: 'email_open_rate', label: 'Email Open Rate', baseline: 18, target: 42, unit: '%', good: 'high' },
  { key: 'whatsapp_response_rate', label: 'WhatsApp Response Rate', baseline: 0, target: 58, unit: '%', good: 'high' },
  { key: 'voice_conversion_rate', label: 'Voice Call Conversion', baseline: 0, target: 31, unit: '%', good: 'high' },
  { key: 'human_escalation_rate', label: 'Human Escalation Rate', baseline: 25, target: 10, unit: '%', good: 'low' },
  { key: 'customer_nps', label: 'Customer NPS', baseline: 34, target: 55, unit: '', good: 'high' },
  { key: 'irdai_violations', label: 'IRDAI Violations', baseline: 12, target: 0, unit: '/yr', good: 'low' },
  { key: 'ai_accuracy_score', label: 'AI Response Accuracy', baseline: 0, target: 87, unit: '%', good: 'high' },
  { key: 'distress_escalation_pct', label: 'Distress Escalated <2h', baseline: 0, target: 100, unit: '%', good: 'high' },
]

function KPICard({ kpiDef, value }: { kpiDef: typeof KPI_DEFS[0]; value: number }) {
  const isGood = kpiDef.good === 'high' ? value >= kpiDef.target : value <= kpiDef.target
  const pct = kpiDef.good === 'high'
    ? Math.min(100, ((value - kpiDef.baseline) / (Math.max(1, kpiDef.target - kpiDef.baseline))) * 100)
    : Math.min(100, ((kpiDef.baseline - value) / (Math.max(1, kpiDef.baseline - kpiDef.target))) * 100)

  return (
    <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-2">
        <p className="text-[10px] text-gray-500 font-bold uppercase tracking-wider leading-tight">{kpiDef.label}</p>
        {isGood ? <CheckCircle className="w-3.5 h-3.5 text-green-500 flex-shrink-0" /> : <AlertCircle className="w-3.5 h-3.5 text-yellow-500 flex-shrink-0" />}
      </div>
      <div className="flex items-end gap-2 mb-2">
        <span className="text-2xl font-bold text-gray-900">{kpiDef.unit === '₹' ? kpiDef.unit : ''}{value.toFixed(kpiDef.unit === '₹' ? 0 : 1)}{kpiDef.unit !== '₹' ? kpiDef.unit : ''}</span>
        <span className={`text-[10px] font-bold mb-1 px-1.5 py-0.5 rounded ${isGood ? 'bg-green-50 text-green-600' : 'bg-yellow-50 text-yellow-600'}`}>
          {isGood ? <TrendingUp className="w-2.5 h-2.5 inline mr-1" /> : <TrendingDown className="w-2.5 h-2.5 inline mr-1" />}
          {((value / kpiDef.baseline - 1) * 100).toFixed(0)}%
        </span>
      </div>
      <div className="w-full bg-gray-100 rounded-full h-1.5 overflow-hidden">
        <div className={`h-1.5 rounded-full transition-all duration-1000 ${isGood ? 'bg-teal-500' : 'bg-yellow-400'}`}
          style={{ width: `${Math.max(5, pct)}%` }} />
      </div>
      <div className="flex justify-between mt-2 text-[9px] font-bold text-gray-400 uppercase">
        <span>Base: {kpiDef.baseline}</span>
        <span>Target: {kpiDef.target}</span>
      </div>
    </div>
  )
}

export default function ExecutiveKPIPage() {
  const { data: kpis, isLoading } = useKPIs()
  const { data: financial } = useFinancial()
  const { data: funnel } = useFunnel()

  if (isLoading) return <div className="flex items-center justify-center h-64 text-gray-400 animate-pulse">Loading real-time performance data...</div>

  return (
    <div className="space-y-6 pt-2">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-black text-gray-900 tracking-tight">Executive Control</h1>
          <p className="text-sm text-gray-500 font-medium">Suraksha RenewAI Performance Dashboard | Multi-Agent Orchestration</p>
        </div>
        <div className="flex gap-4">
          {[
            { label: '3-Yr NPV', value: financial?.npv_3yr ? `₹${financial.npv_3yr} Cr` : '₹89 Cr', icon: Target, color: 'text-teal-700 bg-teal-50' },
            { label: 'Payback', value: financial?.payback_months ? `${financial.payback_months} Mo` : '7.8 Mo', icon: Clock, color: 'text-blue-700 bg-blue-50' },
          ].map(m => (
            <div key={m.label} className={`rounded-xl px-4 py-2 border flex items-center gap-3 shadow-sm ${m.color}`}>
              <m.icon className="w-5 h-5 opacity-70" />
              <div>
                <div className="text-lg font-black leading-none">{m.value}</div>
                <div className="text-[10px] font-bold uppercase tracking-widest">{m.label}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 10 Success KPIs */}
      <div>
        <div className="flex items-center gap-2 mb-3">
          <div className="h-4 w-1 bg-teal-600 rounded-full" />
          <h2 className="text-xs font-black text-gray-400 uppercase tracking-widest">Autonomous Agent Success KPIs</h2>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {KPI_DEFS.map(kd => <KPICard key={kd.key} kpiDef={kd} value={kpis?.[kd.key as keyof typeof kpis] as number ?? 0} />)}
        </div>
      </div>

      {/* Financial + Channel */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-2xl p-6 shadow-sm border hover:shadow-md transition-shadow">
          <h3 className="text-sm font-black text-gray-800 uppercase tracking-widest mb-6">Financial Impact (₹ Crore)</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={financial?.monthly_data || []}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
              <XAxis dataKey="month" tick={{ fontSize: 10, fontWeight: 700 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontSize: 10, fontWeight: 700 }} axisLine={false} tickLine={false} />
              <Tooltip
                contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }}
                formatter={(v: number) => [`₹${v.toFixed(2)} Cr`, '']}
              />
              <Bar dataKey="saving" name="Cost Saving" fill="#0f766e" radius={[4, 4, 0, 0]} barSize={30} />
              <Bar dataKey="revenue" name="Revenue Uplift" fill="#0369a1" radius={[4, 4, 0, 0]} barSize={30} />
            </BarChart>
          </ResponsiveContainer>
          <div className="grid grid-cols-3 gap-4 mt-6">
            {[
              { label: 'Annual Saving', value: `₹${financial?.annual_saving || 12.9} Cr`, color: 'bg-teal-50 text-teal-800' },
              { label: 'Revenue Uplift', value: `₹${financial?.revenue_uplift || 38.9} Cr`, color: 'bg-blue-50 text-blue-800' },
              { label: 'Net Year 1', value: `₹${financial?.net_year1 || 48} Cr`, color: 'bg-gray-900 text-white' },
            ].map(m => (
              <div key={m.label} className={`rounded-xl p-3 text-center border shadow-sm ${m.color}`}>
                <div className="text-base font-black tracking-tight">{m.value}</div>
                <div className="text-[10px] font-bold uppercase tracking-tighter opacity-70">{m.label}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-2xl p-6 shadow-sm border hover:shadow-md transition-shadow">
          <h3 className="text-sm font-black text-gray-800 uppercase tracking-widest mb-6">Conversion Funnel (Current Cycle)</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={funnel || []} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f0f0f0" />
              <XAxis type="number" hide />
              <YAxis dataKey="name" type="category" tick={{ fontSize: 10, fontWeight: 700 }} width={100} axisLine={false} tickLine={false} />
              <Tooltip
                cursor={{ fill: '#f8fafc' }}
                contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }}
                formatter={(v: number) => [v.toLocaleString('en-IN'), 'Customers']}
              />
              <Bar dataKey="value" radius={[0, 4, 4, 0]} barSize={25}>
                {(funnel || []).map((entry: any, i: number) => <Cell key={i} fill={entry.fill} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
          <div className="mt-4 flex flex-wrap gap-2">
            {(funnel || []).map((f: any) => (
              <div key={f.name} className="flex items-center gap-1.5 text-[10px] font-bold text-gray-500 uppercase">
                <div className="w-2 h-2 rounded-full" style={{ background: f.fill }} />
                {f.name}: {f.value}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
