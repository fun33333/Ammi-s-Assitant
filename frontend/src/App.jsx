import { useState, useEffect } from 'react'
import { Home, Package, Settings, ChefHat } from 'lucide-react'
import './index.css'
import './modal.css'
import './suggestions.css'
import ChatPanel from './components/ChatPanel'
import QuickStats from './components/QuickStats'
import RecentMeals from './components/RecentMeals'
import InventoryPreview from './components/InventoryPreview'
import InventoryPage from './components/InventoryPage'
import SuggestedMeals from './components/SuggestedMeals'
import KitchenManager from './components/KitchenManager'

function App() {
  const [stats, setStats] = useState({
    mealsThisWeek: 0,
    totalIngredients: 0,
    nearExpiry: 0
  })
  const [showInventory, setShowInventory] = useState(false)
  const [refreshKey, setRefreshKey] = useState(0)

  const handleRefresh = () => {
    console.log('Refreshing Dashboard...')
    setRefreshKey(prev => prev + 1)
  }

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const invRes = await fetch('http://127.0.0.1:8000/api/agent/inventory/')
        const invData = await invRes.json()
        const mealsRes = await fetch('http://127.0.0.1:8000/api/agent/recent-meals/?days=7')
        const mealsData = await mealsRes.json()

        const nearExpiry = invData.ingredients.filter(ing => ing.urgency === 'high').length

        setStats({
          mealsThisWeek: mealsData.total_meals,
          totalIngredients: invData.total_items,
          nearExpiry: nearExpiry
        })
      } catch (e) {
        console.error('Stats fetch error:', e)
      }
    }
    fetchStats()
  }, [refreshKey])

  return (
    <div className="app">
      <header className="header">
        <div className="logo">
          <ChefHat className="logo-icon" style={{ color: 'var(--primary)' }} />
          Ammi's Assistant
        </div>
        <nav className="nav">
          <button className="nav-btn" onClick={() => setShowInventory(true)}>
            <Package size={18} /> Inventory
          </button>
          <button className="nav-btn">
            <Settings size={18} /> Settings
          </button>
        </nav>
      </header>

      <div className="dashboard">
        <div className="main-content">
          <QuickStats stats={stats} />

          {/* Direct Forms for Adding Ingredients/History */}
          <div style={{ marginBottom: '2rem' }}>
            <KitchenManager onRefresh={handleRefresh} />
          </div>

          {/* Suggestions List */}
          <SuggestedMeals key={`sugg-${refreshKey}`} />

          <RecentMeals key={`meals-${refreshKey}`} />

          <InventoryPreview key={`inv-${refreshKey}`} onViewAll={() => setShowInventory(true)} />
        </div>

        <ChatPanel onMealCooked={handleRefresh} />
      </div>

      {showInventory && (
        <InventoryPage onClose={() => { setShowInventory(false); handleRefresh(); }} />
      )}
    </div>
  )
}

export default App
