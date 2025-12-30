import { useState } from 'react'
import { Plus, X } from 'lucide-react'

function AddIngredientForm({ onClose, onSuccess }) {
    const [formData, setFormData] = useState({
        name: '',
        quantity: '',
        expiry_date: '',
        category: ''
    })
    const [isSubmitting, setIsSubmitting] = useState(false)

    const handleSubmit = async (e) => {
        e.preventDefault()
        setIsSubmitting(true)

        try {
            const response = await fetch('http://127.0.0.1:8000/api/ingredients/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })

            if (response.ok) {
                onSuccess?.()
                onClose()
            } else {
                alert('Failed to add ingredient')
            }
        } catch (error) {
            console.error('Error:', error)
            alert('Error adding ingredient')
        } finally {
            setIsSubmitting(false)
        }
    }

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <div className="modal-header">
                    <h3>Add New Ingredient</h3>
                    <button className="close-btn" onClick={onClose}>
                        <X size={20} />
                    </button>
                </div>

                <form onSubmit={handleSubmit} className="ingredient-form">
                    <div className="form-group">
                        <label>Ingredient Name *</label>
                        <input
                            type="text"
                            required
                            value={formData.name}
                            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                            placeholder="e.g., Tomatoes"
                        />
                    </div>

                    <div className="form-group">
                        <label>Quantity *</label>
                        <input
                            type="text"
                            required
                            value={formData.quantity}
                            onChange={(e) => setFormData({ ...formData, quantity: e.target.value })}
                            placeholder="e.g., 2kg, 500g, 1 dozen"
                        />
                    </div>

                    <div className="form-group">
                        <label>Expiry Date</label>
                        <input
                            type="date"
                            value={formData.expiry_date}
                            onChange={(e) => setFormData({ ...formData, expiry_date: e.target.value })}
                        />
                    </div>

                    <div className="form-group">
                        <label>Category</label>
                        <select
                            value={formData.category}
                            onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                        >
                            <option value="">Select category</option>
                            <option value="Vegetable">Vegetable</option>
                            <option value="Fruit">Fruit</option>
                            <option value="Meat">Meat</option>
                            <option value="Dairy">Dairy</option>
                            <option value="Grain">Grain</option>
                            <option value="Spice">Spice</option>
                            <option value="Other">Other</option>
                        </select>
                    </div>

                    <div className="form-actions">
                        <button type="button" className="btn-secondary" onClick={onClose}>
                            Cancel
                        </button>
                        <button type="submit" className="btn-primary" disabled={isSubmitting}>
                            <Plus size={18} />
                            {isSubmitting ? 'Adding...' : 'Add Ingredient'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}

export default AddIngredientForm
