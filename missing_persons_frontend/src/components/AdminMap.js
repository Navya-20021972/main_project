import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { locationsAPI } from '../services/api';

function AdminMap({ onLocationSelect, blinkingLocationId }) {
  const [locations, setLocations] = useState([]);
  const [blinking, setBlinking] = useState(false);

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

  // Blinking animation for alert zone
  useEffect(() => {
    if (blinkingLocationId) {
      const interval = setInterval(() => {
        setBlinking(prev => !prev);
      }, 500);
      return () => clearInterval(interval);
    } else {
      setBlinking(false);
    }
  }, [blinkingLocationId]);

  // Geofence radius in meters (roughly 100-150m circle around location)
  const GEOFENCE_RADIUS = 100;

  const getZoneColor = (locationId) => {
    if (blinkingLocationId === locationId) {
      return blinking ? '#ff0000' : '#ff6666'; // Red (alert)
    }
    return '#4CAF50'; // Green (normal)
  };

  const getZoneOpacity = (locationId) => {
    if (blinkingLocationId === locationId && blinking) {
      return 0.6; // More opaque when blinking
    }
    return 0.3;
  };

  const getMarkerBackground = (locationId) => {
    if (blinkingLocationId === locationId) {
      return blinking ? '#ff0000' : '#ff6666';
    }
    return '#4CAF50';
  };

  const getMarkerIcon = (locationId, locationName) => {
    const bgColor = getMarkerBackground(locationId);
    
    return L.divIcon({
      html: `<div style="
        background-color: ${bgColor};
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 18px;
        border: 3px solid white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
      ">${locationName[0]}</div>`,
      className: 'zone-marker',
      iconSize: [40, 40],
      popupAnchor: [0, -20]
    });
  };

  return (
    <MapContainer center={[40.7128, -74.0060]} zoom={15} style={{ height: '400px', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; OpenStreetMap contributors'
      />
      
      {locations.map(location => (
        <React.Fragment key={location.id}>
          {/* Geofence Circle */}
          <Circle
            center={[location.latitude, location.longitude]}
            radius={GEOFENCE_RADIUS}
            pathOptions={{
              color: getZoneColor(location.id),
              weight: 2,
              opacity: 1,
              fillColor: getZoneColor(location.id),
              fillOpacity: getZoneOpacity(location.id)
            }}
            eventHandlers={{
              click: () => onLocationSelect(location)
            }}
          >
            <Popup>
              <div style={{ textAlign: 'center' }}>
                <h3>{location.name} Zone</h3>
                <p>{location.description}</p>
                <button 
                  onClick={() => onLocationSelect(location)}
                  style={{
                    backgroundColor: '#2196F3',
                    color: 'white',
                    border: 'none',
                    padding: '0.5rem 1rem',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    fontWeight: 'bold'
                  }}
                >
                  Select This Zone
                </button>
              </div>
            </Popup>
          </Circle>

          {/* Zone Marker/Label */}
          <Marker 
            position={[location.latitude, location.longitude]}
            icon={getMarkerIcon(location.id, location.name)}
            eventHandlers={{
              click: () => onLocationSelect(location)
            }}
          >
            <Popup>
              <div style={{ textAlign: 'center' }}>
                <h3>{location.name} Zone</h3>
                <p>{location.description}</p>
                <button 
                  onClick={() => onLocationSelect(location)}
                  style={{
                    backgroundColor: '#2196F3',
                    color: 'white',
                    border: 'none',
                    padding: '0.5rem 1rem',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    fontWeight: 'bold'
                  }}
                >
                  Select This Zone
                </button>
              </div>
            </Popup>
          </Marker>
        </React.Fragment>
      ))}

      {/* Legend */}
      <div style={{
        position: 'absolute',
        bottom: '10px',
        right: '10px',
        backgroundColor: 'white',
        padding: '1rem',
        borderRadius: '8px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.2)',
        fontSize: '0.85em',
        zIndex: 1000
      }}>
        <div style={{ marginBottom: '0.5rem' }}>
          <span style={{ display: 'inline-block', width: '12px', height: '12px', backgroundColor: '#4CAF50', marginRight: '0.5rem' }}></span>
          Normal Zone
        </div>
        <div>
          <span style={{ display: 'inline-block', width: '12px', height: '12px', backgroundColor: '#ff0000', marginRight: '0.5rem', animation: 'pulse 1s infinite' }}></span>
          Alert Zone
        </div>
      </div>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.4; }
        }
      `}</style>
    </MapContainer>
  );
}

export default AdminMap;
