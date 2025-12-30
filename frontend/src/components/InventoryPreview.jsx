import { useState, useEffect } from 'react'
import { Package, AlertCircle, CheckCircle, Clock, Apple } from 'lucide-react'

function InventoryPreview() {
    const [inventory, setInventory] = useState([])

    useEffect(() => {
        fetchInventory()
    }, [])

    const fetchInventory = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/agent/inventory/')
            const data = await response.json()
            setInventory(data.ingredients.slice(0, 5))
        } catch (error) {
            console.error('Error fetching inventory:', error)
        }
    }

    const getUrgencyIcon = (urgency) => {
        switch (urgency) {
            case 'high':
                return <AlertCircle size={14} />
            case 'medium':
                return <Clock size={14} />
            default:
                return <CheckCircle size={14} />
        }
    }

    const getUrgencyText = (urgency) => {
        switch (urgency) {
            case 'high':
                return 'Expires Soon'
            case 'medium':
                return 'Use Soon'
            default:
                return 'Fresh'
        }
    }

    return (
        <div className="card">
            <div className="card-header">
                <h2 className="card-title">
                    <Package className="card-title-icon" />
                    Current Inventory
                </h2>
                <button className="nav-btn" style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }}>
                    View All →
                </button>
            </div>
            <div className="inventory-list">
                {inventory.length === 0 ? (
                    <div className="empty-state">
                        <Apple className="empty-state-icon" />
                        <p className="empty-state-text">No ingredients yet. Add some to get started!</p>
                    </div>
                ) : (
                    inventory.map((item, idx) => (
                        <div key={idx} className="inventory-item">
                            <div className="inventory-left">
                                <Apple className="inventory-icon" />
                                <div className="inventory-details">
                                    <div className="inventory-name">{item.name}</div>
                                    <div className="inventory-quantity">{item.quantity}</div>
                                </div>
                            </div>
                            {item.urgency && (
                                <span className={`urgency-badge urgency-${item.urgency}`}>
                                    {getUrgencyIcon(item.urgency)}
                                    {getUrgencyText(item.urgency)}
                                </span>
                            )}
                        </div>
                    ))
                )}
            </div>
        </div>
    )
}

export default InventoryPreview
