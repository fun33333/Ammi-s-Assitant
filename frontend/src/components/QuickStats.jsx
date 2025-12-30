import { UtensilsCrossed, Package, AlertTriangle, TrendingUp, TrendingDown } from 'lucide-react'

function QuickStats({ stats }) {
    return (
        <div className="card">
            <div className="card-header">
                <h2 className="card-title">
                    <svg className="card-title-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                    Quick Overview
                </h2>
            </div>
            <div className="stats-grid">
                <div className="stat-card">
                    <div className="stat-header">
                        <UtensilsCrossed className="stat-icon" />
                        <span className="stat-trend up">
                            <TrendingUp size={12} />
                            +12%
                        </span>
                    </div>
                    <div className="stat-value">{stats.mealsThisWeek}</div>
                    <div className="stat-label">Meals This Week</div>
                </div>

                <div className="stat-card">
                    <div className="stat-header">
                        <Package className="stat-icon" />
                        <span className="stat-trend up">
                            <TrendingUp size={12} />
                            +5
                        </span>
                    </div>
                    <div className="stat-value">{stats.totalIngredients}</div>
                    <div className="stat-label">Total Ingredients</div>
                </div>

                <div className="stat-card">
                    <div className="stat-header">
                        <AlertTriangle className="stat-icon" />
                        {stats.nearExpiry > 0 && (
                            <span className="stat-trend down">
                                <TrendingDown size={12} />
                                Alert
                            </span>
                        )}
                    </div>
                    <div className="stat-value">{stats.nearExpiry}</div>
                    <div className="stat-label">Near Expiry</div>
                </div>
            </div>
        </div>
    )
}

export default QuickStats
