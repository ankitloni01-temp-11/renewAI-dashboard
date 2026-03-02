import { useState } from 'react'

interface Objection {
    objection_id?: string
    objection_text: string
    category: string
    response: string
    effectiveness_score: number
}

interface ObjectionLibraryTableProps {
    objections: Objection[]
}

export default function ObjectionLibraryTable({ objections }: ObjectionLibraryTableProps) {
    const [filter, setFilter] = useState('')
    const [categoryFilter, setCategoryFilter] = useState('')

    const categories = [...new Set(objections.map(o => o.category))]
    const filtered = objections.filter(o => {
        const matchText = !filter || o.objection_text.toLowerCase().includes(filter.toLowerCase())
        const matchCat = !categoryFilter || o.category === categoryFilter
        return matchText && matchCat
    })

    return (
        <div>
            <div className="flex gap-3 mb-4">
                <input
                    value={filter} onChange={e => setFilter(e.target.value)}
                    placeholder="Search objections..."
                    className="flex-1 bg-gray-900 border border-gray-600 rounded-lg px-3 py-2 text-sm text-gray-200 placeholder-gray-500 focus:border-blue-500 focus:outline-none"
                />
                <select
                    value={categoryFilter} onChange={e => setCategoryFilter(e.target.value)}
                    className="bg-gray-900 border border-gray-600 rounded-lg px-3 py-2 text-sm text-gray-200"
                >
                    <option value="">All Categories</option>
                    {categories.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
            </div>
            <div className="overflow-x-auto max-h-96 overflow-y-auto">
                <table className="w-full text-sm">
                    <thead className="sticky top-0 bg-gray-800">
                        <tr className="border-b border-gray-700">
                            <th className="text-left py-2 px-3 text-gray-400 font-medium">Objection</th>
                            <th className="text-left py-2 px-3 text-gray-400 font-medium w-32">Category</th>
                            <th className="text-left py-2 px-3 text-gray-400 font-medium">Response</th>
                            <th className="text-center py-2 px-3 text-gray-400 font-medium w-20">Score</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filtered.slice(0, 50).map((o, i) => (
                            <tr key={o.objection_id || i} className="border-b border-gray-800 hover:bg-gray-800/40">
                                <td className="py-2 px-3 text-gray-200">{o.objection_text}</td>
                                <td className="py-2 px-3"><span className="px-2 py-0.5 bg-gray-700 rounded text-xs text-gray-300">{o.category}</span></td>
                                <td className="py-2 px-3 text-gray-400 text-xs max-w-xs truncate">{o.response}</td>
                                <td className="py-2 px-3 text-center">
                                    <span className={`font-semibold ${o.effectiveness_score >= 8 ? 'text-emerald-400' : o.effectiveness_score >= 6 ? 'text-amber-400' : 'text-red-400'}`}>
                                        {o.effectiveness_score}
                                    </span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            <div className="text-xs text-gray-500 mt-2">Showing {Math.min(filtered.length, 50)} of {filtered.length} objections</div>
        </div>
    )
}
