import { useState, useEffect } from 'react'
import { Save, AlertCircle, FileText, CheckCircle2 } from 'lucide-react'
import api from '../api/client'

interface Prompt {
    name: string
    prompt_type: string
    content: string
    version: number
    updated_at: string
}

export default function PromptsPage() {
    const [prompts, setPrompts] = useState<Prompt[]>([])
    const [selectedPrompt, setSelectedPrompt] = useState<Prompt | null>(null)
    const [editContent, setEditContent] = useState('')
    const [loading, setLoading] = useState(true)
    const [saving, setSaving] = useState(false)
    const [notification, setNotification] = useState<{ message: string, type: 'success' | 'error' } | null>(null)

    useEffect(() => {
        fetchPrompts()
    }, [])

    const fetchPrompts = async () => {
        try {
            const { data } = await api.get('/api/prompts')
            setPrompts(data)
            if (data.length > 0 && !selectedPrompt) {
                setSelectedPrompt(data[0])
                setEditContent(data[0].content)
            }
        } catch (err) {
            console.error(err)
            setNotification({ message: 'Failed to fetch prompts', type: 'error' })
        } finally {
            setLoading(false)
        }
    }

    const handleSelect = (prompt: Prompt) => {
        setSelectedPrompt(prompt)
        setEditContent(prompt.content)
        setNotification(null)
    }

    const handleSave = async () => {
        if (!selectedPrompt) return
        setSaving(true)
        try {
            await api.put(`/api/prompts/${selectedPrompt.name}`, { content: editContent })
            setNotification({ message: 'Prompt updated successfully. Agents will use this immediately.', type: 'success' })
            await fetchPrompts()
        } catch (err) {
            console.error(err)
            setNotification({ message: 'Failed to update prompt', type: 'error' })
        } finally {
            setSaving(false)
            setTimeout(() => setNotification(null), 5000)
        }
    }

    if (loading) {
        return <div className="p-8 text-gray-500">Loading prompts...</div>
    }

    return (
        <div className="h-[calc(100vh-64px)] overflow-hidden flex flex-col bg-gray-50">
            <div className="p-6 bg-white border-b border-gray-200 shadow-sm z-10">
                <h1 className="text-2xl font-bold text-gray-800">Prompt Engineering</h1>
                <p className="text-gray-500 mt-1">Manage agent system and user templates dynamically.</p>
            </div>

            <div className="flex-1 flex overflow-hidden">
                {/* Sidebar */}
                <div className="w-80 border-r border-gray-200 bg-white overflow-y-auto">
                    {prompts.map(p => (
                        <button
                            key={p.name}
                            onClick={() => handleSelect(p)}
                            className={`w-full text-left p-4 border-b transition-colors cursor-pointer ${selectedPrompt?.name === p.name ? 'bg-blue-50 border-l-4 border-l-blue-600' : 'hover:bg-gray-50 border-gray-100 border-l-4 border-l-transparent'
                                }`}
                        >
                            <div className="flex items-center gap-2 mb-1">
                                <FileText className="w-4 h-4 text-blue-500" />
                                <span className="font-semibold text-gray-800 text-sm truncate">{p.name}</span>
                            </div>
                            <div className="flex justify-between text-xs text-gray-500">
                                <span>v{p.version}</span>
                                <span>{new Date(p.updated_at).toLocaleDateString()}</span>
                            </div>
                        </button>
                    ))}
                </div>

                {/* Editor */}
                <div className="flex-1 flex flex-col p-6 bg-gray-50 overflow-hidden">
                    {selectedPrompt ? (
                        <div className="bg-white rounded-lg shadow-sm border border-gray-200 flex flex-col h-full">
                            <div className="p-4 border-b border-gray-200 flex justify-between items-center bg-gray-50 rounded-t-lg">
                                <div>
                                    <h2 className="font-bold text-gray-800">{selectedPrompt.name}</h2>
                                    <p className="text-xs text-gray-500 mt-1">Last updated: {new Date(selectedPrompt.updated_at).toLocaleString()}</p>
                                </div>
                                <button
                                    onClick={handleSave}
                                    disabled={saving || editContent === selectedPrompt.content}
                                    className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${saving || editContent === selectedPrompt.content
                                            ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                                            : 'bg-blue-600 hover:bg-blue-700 text-white shadow-sm'
                                        }`}
                                >
                                    <Save className="w-4 h-4" />
                                    {saving ? 'Saving...' : 'Save Changes'}
                                </button>
                            </div>

                            {notification && (
                                <div className={`mx-4 mt-4 p-3 rounded-md text-sm flex items-center gap-2 ${notification.type === 'success' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'
                                    }`}>
                                    {notification.type === 'success' ? <CheckCircle2 className="w-4 h-4" /> : <AlertCircle className="w-4 h-4" />}
                                    {notification.message}
                                </div>
                            )}

                            <div className="flex-1 p-4">
                                <textarea
                                    value={editContent}
                                    onChange={e => setEditContent(e.target.value)}
                                    className="w-full h-full p-4 font-mono text-sm bg-gray-50 border border-gray-200 rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:bg-white resize-none"
                                    spellCheck="false"
                                />
                            </div>
                        </div>
                    ) : (
                        <div className="flex-1 flex items-center justify-center text-gray-500">
                            Select a prompt to edit
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}
