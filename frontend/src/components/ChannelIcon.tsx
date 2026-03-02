import { Mail, MessageCircle, Phone } from 'lucide-react'

interface ChannelIconProps {
    channel: string
    size?: number
}

export default function ChannelIcon({ channel, size = 16 }: ChannelIconProps) {
    const ch = channel?.toLowerCase() || ''
    if (ch.includes('email') || ch.includes('mail'))
        return <Mail size={size} className="text-blue-400" />
    if (ch.includes('whatsapp') || ch.includes('wa'))
        return <MessageCircle size={size} className="text-green-400" />
    if (ch.includes('voice') || ch.includes('call') || ch.includes('phone'))
        return <Phone size={size} className="text-purple-400" />
    return <Mail size={size} className="text-gray-400" />
}
