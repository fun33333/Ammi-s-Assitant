import { useState, useEffect } from 'react'
import { Home, Package, Settings } from 'lucide-react'
import './index.css'
import './modal.css'
import ChatPanel from './components/ChatPanel'
import QuickStats from './components/QuickStats'
import RecentMeals from './components/RecentMeals'
import InventoryPreview from './components/InventoryPreview'
import InventoryPage from './components/InventoryPage'

function App() {
  const [stats, setStats] = useState({
    mealsThisWeek: 0,
    totalIngredients: 0,
    nearExpiry: 0
  })

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const invResponse = await fetch('http://127.0.0.1:8000/api/agent/inventory/')
      const invData = await invResponse.json()

      const mealsResponse = await fetch('http://127.0.0.1:8000/api/agent/recent-meals/?days=7')
      const mealsData = await mealsResponse.json()

      const nearExpiry = invData.ingredients.filter(
        ing => ing.urgency === 'high' || ing.urgency === 'medium'
      ).length

      setStats({
        mealsThisWeek: mealsData.total_meals,
        totalIngredients: invData.total_items,
        nearExpiry: nearExpiry
      })
    } catch (error) {
      console.error('Error fetching stats:', error)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div className="logo">
          <Home className="logo-icon" />
          Ammi's Recipe Assistant
        </div>
        <nav className="nav">
          <button className="nav-btn">
            <Package size={18} />
            Inventory
          </button>
          <button className="nav-btn">
            <Settings size={18} />
            Settings
          </button>
        </nav>
      </header>

      <div className="dashboard">
        <div className="main-content">
          <QuickStats stats={stats} />
          <RecentMeals />
          <InventoryPreview />
        </div>

        <ChatPanel onMealCooked={fetchStats} />
      </div>
    </div>
  )
}

export default App
