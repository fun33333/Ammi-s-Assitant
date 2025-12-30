import { useState, useEffect } from 'react'
import { ChefHat, Clock, Calendar } from 'lucide-react'

function RecentMeals() {
    const [meals, setMeals] = useState([])

    useEffect(() => {
        fetchMeals()
    }, [])

    const fetchMeals = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/agent/recent-meals/?days=2')
            const data = await response.json()
            setMeals(data.meals)
        } catch (error) {
            console.error('Error fetching meals:', error)
        }
    }

    const groupByDate = (meals) => {
        const grouped = {}
        meals.forEach(meal => {
            if (!grouped[meal.date_cooked]) {
                grouped[meal.date_cooked] = []
            }
            grouped[meal.date_cooked].push(meal)
        })
        return grouped
    }

    const formatDate = (dateStr) => {
        const date = new Date(dateStr)
        const today = new Date()
        const yesterday = new Date(today)
        yesterday.setDate(yesterday.getDate() - 1)

        if (date.toDateString() === today.toDateString()) return 'Today'
        if (date.toDateString() === yesterday.toDateString()) return 'Yesterday'
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    }

    const groupedMeals = groupByDate(meals)

    return (
        <div className="card">
            <div className="card-header">
                <h2 className="card-title">
                    <Calendar className="card-title-icon" />
                    Recent Meals
                </h2>
                <span style={{ fontSize: '0.875rem', color: 'var(--text-light)' }}>
                    Last 2 Days
                </span>
            </div>
            <div className="meals-timeline">
                {Object.keys(groupedMeals).length === 0 ? (
                    <div className="empty-state">
                        <ChefHat className="empty-state-icon" />
                        <p className="empty-state-text">No meals recorded yet. Start cooking!</p>
                    </div>
                ) : (
                    Object.entries(groupedMeals).map(([date, dateMeals]) => (
                        <div key={date} className="meal-group">
                            <div className="meal-date-header">
                                <Calendar size={14} />
                                {formatDate(date)}
                            </div>
                            {dateMeals.map((meal, idx) => (
                                <div key={idx} className="meal-item">
                                    <div className="meal-info">
                                        <ChefHat className="meal-icon" />
                                        <div className="meal-name">{meal.name}</div>
                                    </div>
                                    <div className="meal-time">
                                        <Clock size={14} />
                                        {new Date(meal.date_cooked).toLocaleTimeString('en-US', {
                                            hour: '2-digit',
                                            minute: '2-digit'
                                        })}
                                    </div>
                                </div>
                            ))}
                        </div>
                    ))
                )}
            </div>
        </div>
    )
}

export default RecentMeals
