import { useState, useEffect } from 'react'
import { Package, Plus, Trash2, Edit, AlertCircle, CheckCircle, Clock } from 'lucide-react'
import AddIngredientForm from './AddIngredientForm'

function InventoryPage({ onClose }) {
    const [inventory, setInventory] = useState([])
    const [showAddForm, setShowAddForm] = useState(false)
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        fetchInventory()
    }, [])

    const fetchInventory = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/ingredients/')
            const data = await response.json()
            setInventory(data)
        } catch (error) {
            console.error('Error:', error)
        } finally {
            setIsLoading(false)
        }
    }

    const deleteIngredient = async (id) => {
        if (!confirm('Delete this ingredient?')) return

        try {
            const response = await fetch(`http://127.0.0.1:8000/api/ingredients/${id}/`, {
                method: 'DELETE'
            })
            if (response.ok) {
                fetchInventory()
            }
        } catch (error) {
            console.error('Error:', error)
        }
    }

    const getUrgencyBadge = (expiryDate) => {
        if (!expiryDate) return null

        const today = new Date()
        const expiry = new Date(expiryDate)
        const daysLeft = Math.ceil((expiry - today) / (1000 * 60 * 60 * 24))

        if (daysLeft <= 2) {
            return { icon: <AlertCircle size={14} />, text: 'Expires Soon', class: 'urgency-high' }
        } else if (daysLeft <= 5) {
            return { icon: <Clock size={14} />, text: 'Use Soon', class: 'urgency-medium' }
        } else {
            return { icon: <CheckCircle size={14} />, text: 'Fresh', class: 'urgency-low' }
        }
    }

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content large" onClick={(e) => e.stopPropagation()}>
                <div className="modal-header">
                    <h3>
                        <Package size={24} />
                        Full Inventory
                    </h3>
                    <button className="btn-primary" onClick={() => setShowAddForm(true)}>
                        <Plus size={18} />
                        Add Ingredient
                    </button>
                </div>

                <div className="inventory-grid">
                    {isLoading ? (
                        <p>Loading...</p>
                    ) : inventory.length === 0 ? (
                        <div className="empty-state">
                            <Package className="empty-state-icon" />
                            <p className="empty-state-text">No ingredients yet. Add some to get started!</p>
                        </div>
                    ) : (
                        inventory.map((item) => {
                            const urgency = getUrgencyBadge(item.expiry_date)
                            return (
                                <div key={item.id} className="inventory-card">
                                    <div className="inventory-card-header">
                                        <h4>{item.name}</h4>
                                        <button
                                            className="delete-btn"
                                            onClick={() => deleteIngredient(item.id)}
                                        >
                                            <Trash2 size={16} />
                                        </button>
                                    </div>
                                    <div className="inventory-card-body">
                                        <p className="quantity">{item.quantity}</p>
                                        {item.category && <p className="category">{item.category}</p>}
                                        {item.expiry_date && (
                                            <p className="expiry">Expires: {new Date(item.expiry_date).toLocaleDateString()}</p>
                                        )}
                                    </div>
                                    {urgency && (
                                        <div className={`urgency-badge ${urgency.class}`}>
                                            {urgency.icon}
                                            {urgency.text}
                                        </div>
                                    )}
                                </div>
                            )
                        })
                    )}
                </div>
            </div>

            {showAddForm && (
                <AddIngredientForm
                    onClose={() => setShowAddForm(false)}
                    onSuccess={fetchInventory}
                />
            )}
        </div>
    )
}

export default InventoryPage
