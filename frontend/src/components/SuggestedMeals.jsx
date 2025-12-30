import { useState, useEffect } from 'react'
import { Sparkles, ChefHat, Clock, TrendingUp } from 'lucide-react'

function SuggestedMeals() {
    const [suggestions, setSuggestions] = useState([])
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        fetchSuggestions()
    }, [])

    const fetchSuggestions = async () => {
        try {
            // Call the suggestion tool directly
            const response = await fetch('http://127.0.0.1:8000/api/agent/suggestions/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({})
            })
            const data = await response.json()
            setSuggestions(data.suggestions || [])
        } catch (error) {
            console.error('Error:', error)
        } finally {
            setIsLoading(false)
        }
    }

    const markAsCooked = async (mealName) => {
        try {
            await fetch('http://127.0.0.1:8000/api/history/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: mealName
                })
            })
            alert(`${mealName} marked as cooked!`)
        } catch (error) {
            console.error('Error:', error)
        }
    }

    return (
        <div className="card">
            <div className="card-header">
                <h2 className="card-title">
                    <Sparkles className="card-title-icon" />
                    Suggested Meals for Today
                </h2>
                <button className="nav-btn" style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }} onClick={fetchSuggestions}>
                    Refresh
                </button>
            </div>

            {isLoading ? (
                <p style={{ color: 'var(--text-light)', padding: '1rem' }}>Loading suggestions...</p>
            ) : suggestions.length === 0 ? (
                <div className="empty-state">
                    <ChefHat className="empty-state-icon" />
                    <p className="empty-state-text">Add ingredients to get meal suggestions!</p>
                </div>
            ) : (
                <div className="suggestions-grid">
                    {suggestions.map((item, idx) => (
                        <div key={idx} className="suggestion-card">
                            <div className="suggestion-header">
                                <h4>{item.name}</h4>
                                <span className={`match-badge ${item.match_percentage >= 80 ? 'high' : item.match_percentage >= 60 ? 'medium' : 'low'}`}>
                                    <TrendingUp size={14} />
                                    {item.match_percentage}% Match
                                </span>
                            </div>

                            <div className="suggestion-details">
                                <div className="detail-item">
                                    <Clock size={16} />
                                    <span>{item.cooking_time} mins</span>
                                </div>
                                <div className="detail-item">
                                    <ChefHat size={16} />
                                    <span>{item.difficulty}</span>
                                </div>
                            </div>

                            {item.matching_ingredients < item.total_ingredients && (
                                <div className="missing-ingredients">
                                    <p style={{ fontSize: '0.8125rem', color: 'var(--text-light)', marginBottom: '0.25rem' }}>
                                        Missing: {item.total_ingredients - item.matching_ingredients} ingredients
                                    </p>
                                </div>
                            )}

                            <button
                                className="btn-primary"
                                style={{ width: '100%', marginTop: '0.75rem', justifyContent: 'center' }}
                                onClick={() => markAsCooked(item.name)}
                            >
                                <ChefHat size={16} />
                                Mark as Cooked
                            </button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}

export default SuggestedMeals
