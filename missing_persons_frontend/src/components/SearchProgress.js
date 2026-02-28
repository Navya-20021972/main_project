import React, { useEffect, useState } from 'react';
import { searchAPI } from '../services/api';

function SearchProgress({ job }) {
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (job?.status === 'completed') {
      const fetchResults = async () => {
        try {
          const response = await searchAPI.getResults(job.report_id);
          setResults(response.data.results || []);
        } catch (err) {
          setError('Failed to fetch results');
          console.error(err);
        }
      };
      fetchResults();
    }
  }, [job?.status, job?.report_id]);

  if (!job) return null;

  const progress = job.progress || 0;
  const isCompleted = job.status === 'completed';

  return (
    <div style={{ marginTop: '1rem', border: '1px solid #ddd', padding: '1rem', borderRadius: '8px' }}>
      <h4>🔎 Search Status</h4>
      
      {/* Progress Bar */}
      <div style={{ marginBottom: '1rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
          <span>Progress</span>
          <span>{progress}%</span>
        </div>
        <div style={{ width: '100%', height: '20px', backgroundColor: '#eee', borderRadius: '4px', overflow: 'hidden' }}>
          <div 
            style={{ 
              width: `${progress}%`, 
              height: '100%', 
              backgroundColor: '#4CAF50', 
              transition: 'width 0.3s',
              borderRadius: '4px'
            }}
          />
        </div>
        <p style={{ fontSize: '0.9em', color: '#666', marginTop: '0.5rem' }}>
          Status: <strong>{job.status}</strong> | Videos: {job.videos_processed || 0} / {job.total_videos || 0}
        </p>
      </div>

      {/* Error Message */}
      {job.error_message && (
        <div style={{ backgroundColor: '#fee', padding: '0.75rem', borderRadius: '4px', marginBottom: '1rem', color: '#c00' }}>
          ❌ {job.error_message}
        </div>
      )}

      {/* Results */}
      {isCompleted && (
        <div>
          <h5>🎯 Results ({results.length} matches found)</h5>
          {results.length === 0 ? (
            <p style={{ color: '#999', fontStyle: 'italic' }}>No matches found in the searched videos.</p>
          ) : (
            <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
              {results.map((result, idx) => (
                <div 
                  key={idx}
                  style={{
                    border: '1px solid #ccc',
                    padding: '0.75rem',
                    marginBottom: '0.75rem',
                    borderRadius: '4px',
                    backgroundColor: '#f9f9f9'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                    <strong>{result.camera_name}</strong>
                    <span style={{ backgroundColor: '#4CAF50', color: 'white', padding: '0.25rem 0.5rem', borderRadius: '4px', fontSize: '0.9em' }}>
                      {(result.confidence * 100).toFixed(1)}% match
                    </span>
                  </div>
                  <p style={{ margin: '0.25rem 0', fontSize: '0.9em' }}>
                    📍 Zone: {result.location_name}
                  </p>
                  <p style={{ margin: '0.25rem 0', fontSize: '0.9em' }}>
                    ⏰ Time: {new Date(result.match_time).toLocaleString()}
                  </p>
                  {result.face_snapshot && (
                    <img 
                      src={result.face_snapshot} 
                      alt="Match" 
                      style={{ maxWidth: '100%', marginTop: '0.5rem', borderRadius: '4px' }}
                    />
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default SearchProgress;
