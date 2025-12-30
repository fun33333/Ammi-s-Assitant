import { useState, useRef, useEffect } from 'react'
import { MessageCircle, Send, Loader2, AlertCircle } from 'lucide-react'

function ChatPanel({ onMealCooked }) {
    const [messages, setMessages] = useState([
        { role: 'assistant', content: 'Assalam o Alaikum! Aaj khanay mein kya banana hai?' }
    ])
    const [input, setInput] = useState('')
    const [isLoading, setIsLoading] = useState(false)
    const [conversationHistory, setConversationHistory] = useState([])
    const messagesEndRef = useRef(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    useEffect(() => {
        scrollToBottom()
    }, [messages])

    const sendMessage = async () => {
        if (!input.trim() || isLoading) return

        const userMessage = input.trim()
        setInput('')

        setMessages(prev => [...prev, { role: 'user', content: userMessage }])
        setIsLoading(true)

        try {
            const response = await fetch('http://127.0.0.1:8000/api/agent/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: userMessage,
                    conversation_history: conversationHistory
                })
            })

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`)
            }

            const data = await response.json()

            // Check if there's an error in the response
            if (data.error) {
                console.error('API Error:', data.error)
            }

            setMessages(prev => [...prev, {
                role: 'assistant',
                content: data.reply,
                hasError: !!data.error
            }])
            setConversationHistory(data.conversation_history)

            if (userMessage.toLowerCase().includes('cooked') ||
                userMessage.toLowerCase().includes('bana liya')) {
                onMealCooked?.()
            }
        } catch (error) {
            console.error('Error:', error)
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: 'Sorry, I could not connect to the server. Please make sure the backend is running.',
                hasError: true
            }])
        } finally {
            setIsLoading(false)
        }
    }

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            sendMessage()
        }
    }

    return (
        <div className="chat-panel">
            <div className="chat-header">
                <MessageCircle className="chat-header-icon" />
                <span className="chat-header-title">Ammi's AI Assistant</span>
            </div>

            <div className="chat-messages">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`message ${msg.role}`}>
                        {msg.hasError && (
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                                <AlertCircle size={16} color="#EF4444" />
                                <span style={{ fontSize: '0.75rem', color: '#EF4444' }}>Service Issue</span>
                            </div>
                        )}
                        {msg.content}
                    </div>
                ))}
                {isLoading && (
                    <div className="message typing">
                        <Loader2 size={16} className="animate-spin" style={{ animation: 'spin 1s linear infinite' }} />
                        Typing...
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <div className="chat-input-container">
                <input
                    type="text"
                    className="chat-input"
                    placeholder="Ask me anything..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    disabled={isLoading}
                />
                <button
                    className="send-btn"
                    onClick={sendMessage}
                    disabled={isLoading || !input.trim()}
                >
                    <Send size={18} />
                </button>
            </div>
        </div>
    )
}

export default ChatPanel
