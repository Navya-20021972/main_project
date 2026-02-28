import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

function AdminMap({ onLocationSelect }) {
  const [locations, setLocations] = useState([]);

  useEffect(() => {
    // TODO: Fetch locations from backend
    // For now, sample data
    setLocations([
      { id: 1, name: 'Library', latitude: 40.7128, longitude: -74.0060 },
      { id: 2, name: 'Canteen', latitude: 40.7131, longitude: -74.0055 },
      { id: 3, name: 'Parking', latitude: 40.7125, longitude: -74.0065 }
    ]);
  }, []);

  return (
    <MapContainer center={[40.7128, -74.0060]} zoom={15} style={{ height: '400px', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; OpenStreetMap contributors'
      />
      {locations.map(location => (
        <Marker key={location.id} position={[location.latitude, location.longitude]}>
          <Popup>
            <div>
              <h3>{location.name}</h3>
              <button onClick={() => onLocationSelect(location)}>
                Select This Zone
              </button>
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}

export default AdminMap;
