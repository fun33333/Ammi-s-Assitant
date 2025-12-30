import { useState, useEffect } from 'react'
import { Sparkles, ChefHat, Clock, TrendingUp, RefreshCw } from 'lucide-react'

function SuggestedMeals() {
    const [suggestions, setSuggestions] = useState([])
    const [isLoading, setIsLoading] = useState(true)

    const fetchSuggestions = async () => {
        setIsLoading(true)
        try {
            const response = await fetch('http://127.0.0.1:8000/api/agent/suggestions/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            })
            const data = await response.json()
            console.log('Suggestions Data:', data) // Debugging
            setSuggestions(data.suggestions || [])
        } catch (error) {
            console.error('Error fetching suggestions:', error)
        } finally {
            setIsLoading(false)
        }
    }

    useEffect(() => {
        fetchSuggestions()
    }, [])

    const markAsCooked = async (mealName) => {
        try {
            await fetch('http://127.0.0.1:8000/api/history/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: mealName })
            })
            alert(`Wah! ${mealName} paka liya!`)
            fetchSuggestions()
        } catch (error) {
            console.error('Error marking as cooked:', error)
        }
    }

    return (
        <div className="card" style={{ marginBottom: '2rem' }}>
            <div className="card-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h2 className="card-title" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <Sparkles className="card-title-icon" style={{ color: 'var(--primary)' }} />
                    Ammi ki Suggestions
                </h2>
                <button className="nav-btn" onClick={fetchSuggestions} disabled={isLoading}>
                    <RefreshCw size={14} className={isLoading ? 'spin' : ''} /> Refresh
                </button>
            </div>

            {isLoading ? (
                <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-light)' }}>
                    Ma'am thoda soch rahi hain...
                </div>
            ) : suggestions.length === 0 ? (
                <div className="empty-state" style={{ padding: '2rem' }}>
                    <ChefHat className="empty-state-icon" style={{ opacity: 0.3 }} />
                    <p className="empty-state-text">Ghar mein kuch nahi hai? Thode ingredients add karein!</p>
                </div>
            ) : (
                <div className="suggestions-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem', padding: '1rem' }}>
                    {suggestions.map((item, idx) => (
                        <div key={idx} className="suggestion-card" style={{
                            background: 'white',
                            border: '1px solid var(--border)',
                            borderRadius: '12px',
                            padding: '1rem',
                            boxShadow: '0 2px 4px rgba(0,0,0,0.05)'
                        }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                <h4 style={{ margin: 0, color: 'var(--text)' }}>{item.name}</h4>
                                <span className={`match-badge ${item.match_percentage >= 50 ? 'high' : 'medium'}`} style={{
                                    padding: '2px 8px', borderRadius: '4px', fontSize: '0.75rem', fontWeight: 'bold',
                                    background: item.match_percentage >= 50 ? '#DCFCE7' : '#FEF3C7',
                                    color: item.match_percentage >= 50 ? '#166534' : '#92400E'
                                }}>
                                    {item.match_percentage}% Match
                                </span>
                            </div>

                            <div style={{ display: 'flex', gap: '0.75rem', fontSize: '0.875rem', color: 'var(--text-light)', marginBottom: '1rem' }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                                    <Clock size={14} /> {item.cooking_time}m
                                </div>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                                    <ChefHat size={14} /> {item.difficulty}
                                </div>
                            </div>

                            <button
                                className="btn-primary"
                                onClick={() => markAsCooked(item.name)}
                                style={{ width: '100%', justifyContent: 'center', padding: '0.5rem' }}
                            >
                                Paka Diya!
                            </button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}

export default SuggestedMeals
