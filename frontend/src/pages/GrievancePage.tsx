export default function GrievancePage() {
  const grievances = [
    { id: 'GRV-001', customer: 'Suresh Mehta', type: 'Mis-selling', date: '2026-02-10', status: 'Resolved', sla: 15, days_taken: 8 },
    { id: 'GRV-002', customer: 'Kamala Devi', type: 'Wrong Deduction', date: '2026-02-20', status: 'In Progress', sla: 15, days_taken: 10 },
    { id: 'GRV-003', customer: 'Arjun Naik', type: 'Service Complaint', date: '2026-02-28', status: 'Open', sla: 15, days_taken: 2 },
  ]
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div><h1 className="text-2xl font-bold text-gray-900">Grievance Register</h1><p className="text-sm text-gray-500">IRDAI SLA: 15 days | Violations YTD: 0</p></div>
        <div className="flex gap-2">
          <button className="text-sm bg-[#1B4F8A] text-white px-3 py-2 rounded-lg">Monthly Report</button>
          <button className="text-sm bg-gray-100 text-gray-700 px-3 py-2 rounded-lg border">Quarterly Report</button>
        </div>
      </div>
      <div className="grid grid-cols-4 gap-4">
        {[{ l: 'IRDAI Violations', v: '0', c: 'text-green-700 bg-green-50' },{ l: 'Active Grievances', v: '2', c: 'text-yellow-700 bg-yellow-50' },{ l: 'Avg Resolution', v: '8.2 days', c: 'text-blue-700 bg-blue-50' },{ l: 'IRDAI SLA', v: '15 days', c: 'text-gray-700 bg-gray-50' }].map(c => (
          <div key={c.l} className={`${c.c} rounded-xl p-4 border`}><div className={`text-2xl font-bold`}>{c.v}</div><div className="text-xs text-gray-500">{c.l}</div></div>
        ))}
      </div>
      <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b"><tr>{['ID','Customer','Type','Date Filed','SLA','Days Taken','Status'].map(h => <th key={h} className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase">{h}</th>)}</tr></thead>
          <tbody>{grievances.map(g => (
            <tr key={g.id} className="border-b hover:bg-gray-50">
              <td className="px-4 py-3 font-medium text-blue-700">{g.id}</td>
              <td className="px-4 py-3">{g.customer}</td>
              <td className="px-4 py-3">{g.type}</td>
              <td className="px-4 py-3 text-gray-500">{g.date}</td>
              <td className="px-4 py-3">{g.sla} days</td>
              <td className="px-4 py-3"><span className={g.days_taken > g.sla ? 'text-red-600' : 'text-green-600'}>{g.days_taken} days</span></td>
              <td className="px-4 py-3"><span className={`px-2 py-0.5 rounded text-xs font-medium ${g.status==='Resolved' ? 'bg-green-100 text-green-700' : g.status==='In Progress' ? 'bg-yellow-100 text-yellow-700' : 'bg-gray-100 text-gray-700'}`}>{g.status}</span></td>
            </tr>
          ))}</tbody>
        </table>
      </div>
    </div>
  )
}
