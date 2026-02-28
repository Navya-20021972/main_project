import React from 'react';

function SearchProgress() {
  return (
    <div className="card">
      <h3>Search in Progress</h3>
      <div style={{ marginTop: '1rem' }}>
        <div style={{ marginBottom: '0.5rem' }}>
          <label>Processed: 3 / 10 videos</label>
          <div style={{ width: '100%', height: '20px', backgroundColor: '#eee', borderRadius: '4px', overflow: 'hidden' }}>
            <div style={{ width: '30%', height: '100%', backgroundColor: '#667eea', transition: 'width 0.3s' }}></div>
          </div>
        </div>
        <p style={{ color: '#666' }}>Matches found: 0</p>
      </div>
    </div>
  );
}

export default SearchProgress;
