import React, { useState, useEffect } from 'react';

function CameraSelector({ locationId, onCamerasSelect }) {
  const [cameras, setCameras] = useState([]);
  const [selectedCameras, setSelectedCameras] = useState([]);

  useEffect(() => {
    // TODO: Fetch cameras for location from backend
    console.log('Fetching cameras for location:', locationId);
  }, [locationId]);

  const handleCameraToggle = (cameraId) => {
    if (selectedCameras.includes(cameraId)) {
      setSelectedCameras(selectedCameras.filter(id => id !== cameraId));
    } else {
      setSelectedCameras([...selectedCameras, cameraId]);
    }
    onCamerasSelect(selectedCameras);
  };

  return (
    <div>
      {cameras.length === 0 ? (
        <p>No cameras found for this location</p>
      ) : (
        cameras.map(camera => (
          <div key={camera.id} style={{ padding: '0.5rem', border: '1px solid #ddd', marginBottom: '0.5rem' }}>
            <input
              type="checkbox"
              checked={selectedCameras.includes(camera.id)}
              onChange={() => handleCameraToggle(camera.id)}
            />
            <label style={{ marginLeft: '0.5rem' }}>{camera.name}</label>
          </div>
        ))
      )}
    </div>
  );
}

export default CameraSelector;
