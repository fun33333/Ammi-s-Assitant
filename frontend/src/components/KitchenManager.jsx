import { useState } from 'react'
import { Plus, ChefHat, Package, History } from 'lucide-react'

function KitchenManager({ onRefresh }) {
    const [activeTab, setActiveTab] = useState('ingredient')
    const [formData, setFormData] = useState({
        name: '',
        quantity: '',
        expiry_date: '',
        category: ''
    })
    const [mealData, setMealData] = useState({
        name: '',
        ingredients_used: ''
    })
    const [isSubmitting, setIsSubmitting] = useState(false)

    const handleAddIngredient = async (e) => {
        e.preventDefault()
        setIsSubmitting(true)
        try {
            const response = await fetch('http://127.0.0.1:8000/api/ingredients/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            })
            if (response.ok) {
                setFormData({ name: '', quantity: '', expiry_date: '', category: '' })
                onRefresh?.()
                alert('Ingredient added!')
            }
        } catch (error) {
            console.error(error)
        } finally {
            setIsSubmitting(false)
        }
    }

    const handleAddMeal = async (e) => {
        e.preventDefault()
        setIsSubmitting(true)
        try {
            const response = await fetch('http://127.0.0.1:8000/api/history/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(mealData)
            })
            if (response.ok) {
                setMealData({ name: '', ingredients_used: '' })
                onRefresh?.()
                alert('Meal history updated!')
            }
        } catch (error) {
            console.error(error)
        } finally {
            setIsSubmitting(false)
        }
    }

    return (
        <div className="card" style={{ marginBottom: '2rem', border: '2px solid var(--primary)', background: '#fff', borderRadius: '16px', overflow: 'hidden' }}>
            <div className="card-header" style={{ background: '#FFF5EB', borderBottom: '1px solid var(--border)', padding: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h3 className="card-title" style={{ color: 'var(--primary)', margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <ChefHat size={22} /> Kitchen Management
                </h3>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <button
                        className={`nav-btn ${activeTab === 'ingredient' ? 'active' : ''}`}
                        onClick={() => setActiveTab('ingredient')}
                        style={{
                            background: activeTab === 'ingredient' ? 'var(--primary)' : 'transparent',
                            color: activeTab === 'ingredient' ? 'white' : 'var(--text)',
                            borderColor: 'var(--primary)',
                            padding: '0.5rem 1rem',
                            borderRadius: '8px',
                            fontSize: '0.9rem',
                            fontWeight: '600'
                        }}
                    >
                        <Package size={16} /> Add Ingredient
                    </button>
                    <button
                        className={`nav-btn ${activeTab === 'meal' ? 'active' : ''}`}
                        onClick={() => setActiveTab('meal')}
                        style={{
                            background: activeTab === 'meal' ? 'var(--primary)' : 'transparent',
                            color: activeTab === 'meal' ? 'white' : 'var(--text)',
                            borderColor: 'var(--primary)',
                            padding: '0.5rem 1rem',
                            borderRadius: '8px',
                            fontSize: '0.9rem',
                            fontWeight: '600'
                        }}
                    >
                        <History size={16} /> Record Meal
                    </button>
                </div>
            </div>

            <div style={{ padding: '1.5rem' }}>
                {activeTab === 'ingredient' ? (
                    <form onSubmit={handleAddIngredient} className="ingredient-form" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.25rem' }}>
                        <div className="form-group">
                            <label style={{ color: 'var(--text)', fontWeight: '600', marginBottom: '0.25rem' }}>Ingredient Name</label>
                            <input
                                value={formData.name}
                                onChange={e => setFormData({ ...formData, name: e.target.value })}
                                placeholder="e.g. Tomatoes, Basmati Rice"
                                required
                                style={{ border: '1px solid var(--border)', padding: '0.75rem', borderRadius: '8px' }}
                            />
                        </div>
                        <div className="form-group">
                            <label style={{ color: 'var(--text)', fontWeight: '600', marginBottom: '0.25rem' }}>Quantity & Unit</label>
                            <input
                                value={formData.quantity}
                                onChange={e => setFormData({ ...formData, quantity: e.target.value })}
                                placeholder="e.g. 1kg, 2 packs"
                                required
                                style={{ border: '1px solid var(--border)', padding: '0.75rem', borderRadius: '8px' }}
                            />
                        </div>
                        <div className="form-group">
                            <label style={{ color: 'var(--text)', fontWeight: '600', marginBottom: '0.25rem' }}>Expiry Date</label>
                            <input
                                type="date"
                                value={formData.expiry_date}
                                onChange={e => setFormData({ ...formData, expiry_date: e.target.value })}
                                style={{ border: '1px solid var(--border)', padding: '0.75rem', borderRadius: '8px' }}
                            />
                        </div>
                        <div className="form-group">
                            <label style={{ color: 'var(--text)', fontWeight: '600', marginBottom: '0.25rem' }}>Category</label>
                            <select
                                value={formData.category}
                                onChange={e => setFormData({ ...formData, category: e.target.value })}
                                style={{ border: '1px solid var(--border)', padding: '0.75rem', borderRadius: '8px', background: '#fff' }}
                            >
                                <option value="">Select Category</option>
                                <option value="Veg">Vegetable</option>
                                <option value="Fruit">Fruit</option>
                                <option value="Dairy">Dairy</option>
                                <option value="Meat">Meat</option>
                                <option value="Spice">Spice</option>
                                <option value="Pantry">Pantry/Grains</option>
                            </select>
                        </div>
                        <button type="submit" className="btn-primary" style={{ gridColumn: '1 / -1', padding: '1rem', fontSize: '1rem', background: 'var(--primary)', border: 'none', color: 'white', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }} disabled={isSubmitting}>
                            {isSubmitting ? 'Processing...' : '✅ Save to My Kitchen'}
                        </button>
                    </form>
                ) : (
                    <form onSubmit={handleAddMeal} className="ingredient-form" style={{ maxWidth: '600px', margin: '0 auto' }}>
                        <div className="form-group" style={{ marginBottom: '1rem' }}>
                            <label style={{ color: 'var(--text)', fontWeight: '600', marginBottom: '0.25rem' }}>What did you cook today?</label>
                            <input
                                value={mealData.name}
                                onChange={e => setMealData({ ...mealData, name: e.target.value })}
                                placeholder="e.g. Chicken Biryani, Aloo Gobi"
                                required
                                style={{ border: '1px solid var(--border)', padding: '0.75rem', borderRadius: '8px', width: '100%' }}
                            />
                        </div>
                        <div className="form-group" style={{ marginBottom: '1rem' }}>
                            <label style={{ color: 'var(--text)', fontWeight: '600', marginBottom: '0.25rem' }}>Any special ingredients used?</label>
                            <textarea
                                value={mealData.ingredients_used}
                                onChange={e => setMealData({ ...mealData, ingredients_used: e.target.value })}
                                placeholder="e.g. Saffron, Special Masala..."
                                style={{ border: '1px solid var(--border)', borderRadius: '8px', padding: '0.75rem', minHeight: '80px', width: '100%', fontFamily: 'inherit' }}
                            />
                        </div>
                        <button type="submit" className="btn-primary" style={{ width: '100%', padding: '1rem', fontSize: '1rem', background: 'var(--primary)', border: 'none', color: 'white', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }} disabled={isSubmitting}>
                            {isSubmitting ? 'Recording...' : '🥘 Record this Meal'}
                        </button>
                    </form>
                )}
            </div>
        </div>
    )
}

export default KitchenManager
