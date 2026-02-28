import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { locationsAPI } from '../services/api';

function AdminMap({ onLocationSelect, blinkingLocationId }) {
  const [locations, setLocations] = useState([]);
  const [blinking, setBlinking] = useState({});

  useEffect(() => {
    const fetchLocations = async () => {
      try {
        const response = await locationsAPI.getLocations();
        setLocations(response.data.results || []);
      } catch (err) {
        console.error('Error fetching locations:', err);
      }
    };
    fetchLocations();
  }, []);

  // Handle blinking effect
  useEffect(() => {
    if (blinkingLocationId) {
      const interval = setInterval(() => {
        setBlinking(prev => ({
          ...prev,
          [blinkingLocationId]: !prev[blinkingLocationId]
        }));
      }, 500); // Blink every 500ms
      return () => clearInterval(interval);
    }
  }, [blinkingLocationId]);

  const getMarkerIcon = (locationId) => {
    const isBlinking = blinkingLocationId === locationId && blinking[locationId];
    const color = isBlinking ? '#ff0000' : '#4CAF50';
    const opacity = isBlinking ? 0.8 : 1;
    
    return L.divIcon({
      html: `<div style="
        background-color: ${color};
        width: 30px;
        height: 30px;
        border-radius: 50%;
        border: 3px solid ${color};
        opacity: ${opacity};
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0 0 ${isBlinking ? '15px' : '5px'} ${color};
        transition: all 0.3s ease;
      ">📍</div>`,
      className: 'custom-div-icon',
      iconSize: [30, 30],
      popupAnchor: [0, -15]
    });
  };

  return (
    <MapContainer center={[40.7128, -74.0060]} zoom={15} style={{ height: '400px', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; OpenStreetMap contributors'
      />
      {locations.map(location => (
        <Marker 
          key={location.id} 
          position={[location.latitude, location.longitude]}
          icon={getMarkerIcon(location.id)}
        >
          <Popup>
            <div>
              <h3>{location.name}</h3>
              <p>{location.description}</p>
              <button 
                onClick={() => onLocationSelect(location)}
                style={{
                  backgroundColor: '#2196F3',
                  color: 'white',
                  border: 'none',
                  padding: '0.5rem 1rem',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
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
