import React, { useState, useEffect } from 'react';
import { suggestionsAPI, shoppingAPI } from '../api';
import './Suggestions.css';

export function Suggestions({ onAddItem, loading }) {
  const [suggestions, setSuggestions] = useState([]);
  const [loadingSuggestions, setLoadingSuggestions] = useState(false);

  useEffect(() => {
    fetchSuggestions();
  }, []);

  const fetchSuggestions = async () => {
    setLoadingSuggestions(true);
    try {
      const response = await suggestionsAPI.getSmartSuggestions();
      setSuggestions(response.data.suggestions || []);
    } catch (error) {
      console.error('Failed to fetch suggestions:', error);
    } finally {
      setLoadingSuggestions(false);
    }
  };

  const getSuggestionIcon = (type) => {
    const icons = {
      'history_based': '📊',
      'seasonal': '🌱',
      'substitute': '🔄'
    };
    return icons[type] || '💡';
  };

  const handleAddSuggestion = (suggestion) => {
    onAddItem({
      item_name: suggestion.item,
      category: suggestion.category,
      quantity: 1
    });
  };

  return (
    <div className="suggestions">
      <div className="suggestions-header">
        <h3>Smart Suggestions</h3>
        <button
          className="refresh-btn"
          onClick={fetchSuggestions}
          disabled={loading || loadingSuggestions}
        >
          🔄
        </button>
      </div>

      {suggestions.length === 0 ? (
        <p className="no-suggestions">No suggestions yet. Start adding items!</p>
      ) : (
        <div className="suggestion-list">
          {suggestions.map((suggestion, idx) => (
            <div key={idx} className="suggestion-item">
              <div className="suggestion-content">
                <span className="suggestion-icon">
                  {getSuggestionIcon(suggestion.suggestion_type)}
                </span>
                <div className="suggestion-info">
                  <div className="suggestion-title">{suggestion.item}</div>
                  <div className="suggestion-reason">{suggestion.reason}</div>
                </div>
              </div>
              <button
                className="add-suggestion-btn"
                onClick={() => handleAddSuggestion(suggestion)}
                disabled={loading}
              >
                + Add
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
