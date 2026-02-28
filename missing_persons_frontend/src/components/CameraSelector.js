import React, { useState, useEffect } from 'react';
import { locationsAPI } from '../services/api';

function CameraSelector({ locationId, onCamerasSelect }) {
  const [cameras, setCameras] = useState([]);
  const [selectedCameras, setSelectedCameras] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!locationId) {
      setCameras([]);
      return;
    }

    const fetchCameras = async () => {
      setLoading(true);
      try {
        const response = await locationsAPI.getCameras(locationId);
        setCameras(response.data.results || []);
        setSelectedCameras([]); // Reset selection when location changes
      } catch (err) {
        console.error('Error fetching cameras:', err);
        setCameras([]);
      } finally {
        setLoading(false);
      }
    };

    fetchCameras();
  }, [locationId]);

  const handleCameraToggle = (cameraId) => {
    let updated;
    if (selectedCameras.includes(cameraId)) {
      updated = selectedCameras.filter(id => id !== cameraId);
    } else {
      updated = [...selectedCameras, cameraId];
    }
    setSelectedCameras(updated);
    onCamerasSelect(updated);
  };

  if (loading) {
    return <p>Loading cameras...</p>;
  }

  if (cameras.length === 0) {
    return <p style={{ color: '#999', fontStyle: 'italic' }}>No cameras available for this location</p>;
  }

  return (
    <div>
      {cameras.map(camera => (
        <div 
          key={camera.id} 
          style={{ 
            padding: '0.75rem', 
            border: '1px solid #ddd', 
            marginBottom: '0.5rem',
            borderRadius: '4px',
            backgroundColor: selectedCameras.includes(camera.id) ? '#e3f2fd' : '#fff'
          }}
        >
          <input
            type="checkbox"
            id={`camera-${camera.id}`}
            checked={selectedCameras.includes(camera.id)}
            onChange={() => handleCameraToggle(camera.id)}
            style={{ cursor: 'pointer' }}
          />
          <label 
            htmlFor={`camera-${camera.id}`}
            style={{ marginLeft: '0.5rem', cursor: 'pointer' }}
          >
            <strong>{camera.name}</strong>
          </label>
          {camera.description && (
            <p style={{ margin: '0.25rem 0 0 1.5rem', fontSize: '0.85em', color: '#666' }}>
              {camera.description}
            </p>
          )}
        </div>
      ))}
      <div style={{ marginTop: '1rem', padding: '0.75rem', backgroundColor: '#f5f5f5', borderRadius: '4px' }}>
        <strong>Selected: {selectedCameras.length} camera(s)</strong>
      </div>
    </div>
  );
}

export default CameraSelector;
