import React, { useState, useEffect } from 'react';
import '../App.css';
import AdminMap from '../components/AdminMap';
import CameraSelector from '../components/CameraSelector';
import SearchProgress from '../components/SearchProgress';

function AdminDashboard() {
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [selectedCameras, setSelectedCameras] = useState([]);
  const [isSearching, setIsSearching] = useState(false);

  return (
    <div className="container">
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '2rem' }}>
        <div className="card">
          <h2>Locations</h2>
          <AdminMap onLocationSelect={setSelectedLocation} />
        </div>
        
        <div>
          <div className="card">
            <h2>Cameras in {selectedLocation?.name || 'Select a location'}</h2>
            {selectedLocation && (
              <CameraSelector 
                locationId={selectedLocation.id} 
                onCamerasSelect={setSelectedCameras}
              />
            )}
          </div>
          
          {isSearching && <SearchProgress />}
        </div>
      </div>
    </div>
  );
}

export default AdminDashboard;
