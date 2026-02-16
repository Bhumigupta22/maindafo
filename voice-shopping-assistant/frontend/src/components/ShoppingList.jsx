import React, { useState, useEffect } from 'react';
import { shoppingAPI } from '../api';
import './ShoppingList.css';

export function ShoppingList({ items, onItemRemove, onItemComplete, loading }) {
  const [expandedCategory, setExpandedCategory] = useState(null);

  // Group items by category
  const groupedItems = items.reduce((acc, item) => {
    const category = item.category || 'Other';
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(item);
    return acc;
  }, {});

  const getCategoryEmoji = (category) => {
    const emojis = {
      'dairy': '🥛',
      'produce': '🥬',
      'meat': '🥩',
      'snacks': '🍪',
      'beverages': '🥤',
      'pantry': '🍞',
      'other': '📦'
    };
    return emojis[category] || '📦';
  };

  return (
    <div className="shopping-list">
      <h2>Shopping List</h2>
      {items.length === 0 ? (
        <p className="empty-state">No items yet. Add some using voice commands!</p>
      ) : (
        <div className="categories">
          {Object.entries(groupedItems).map(([category, categoryItems]) => (
            <div key={category} className="category-group">
              <button
                className="category-header"
                onClick={() => setExpandedCategory(
                  expandedCategory === category ? null : category
                )}
              >
                <span className="category-emoji">{getCategoryEmoji(category)}</span>
                <span className="category-name">{category}</span>
                <span className="item-count">{categoryItems.length}</span>
                <span className="toggle">
                  {expandedCategory === category ? '▼' : '▶'}
                </span>
              </button>
              
              {expandedCategory === category && (
                <div className="items">
                  {categoryItems.map(item => (
                    <div key={item.id} className="item">
                      <div className="item-details">
                        <div className="item-name">{item.item_name}</div>
                        {item.quantity && (
                          <div className="item-quantity">
                            {item.quantity} {item.unit}
                          </div>
                        )}
                      </div>
                      <div className="item-actions">
                        <button
                          className="action-btn complete"
                          onClick={() => onItemComplete(item.id)}
                          disabled={loading}
                          title="Mark as purchased"
                        >
                          ✓
                        </button>
                        <button
                          className="action-btn remove"
                          onClick={() => onItemRemove(item.id)}
                          disabled={loading}
                          title="Remove item"
                        >
                          ✕
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
