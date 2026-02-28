import React, { useState, useEffect } from 'react';
import '../App.css';
import AdminMap from '../components/AdminMap';
import CameraSelector from '../components/CameraSelector';
import SearchProgress from '../components/SearchProgress';
import { reportAPI, searchAPI } from '../services/api';

function AdminDashboard() {
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [selectedCameras, setSelectedCameras] = useState([]);
  const [reports, setReports] = useState([]);
  const [selectedReport, setSelectedReport] = useState(null);
  const [searchJob, setSearchJob] = useState(null);
  const [isSearching, setIsSearching] = useState(false);
  const [newReportLocation, setNewReportLocation] = useState(null);
  const [uploadedVideos, setUploadedVideos] = useState({});

  // Fetch reports and poll for new ones
  useEffect(() => {
    const fetchReports = async () => {
      try {
        const response = await reportAPI.getReports();
        const newReports = response.data.results || [];
        setReports(newReports);
        
        // Highlight location of newest unfound report
        const unfoundReports = newReports.filter(r => r.status !== 'found');
        if (unfoundReports.length > 0) {
          setNewReportLocation(unfoundReports[0].last_seen_location);
        }
      } catch (err) {
        console.error('Error fetching reports:', err);
      }
    };

    fetchReports();
    const interval = setInterval(fetchReports, 5000); // Poll every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const handleStartSearch = async () => {
    if (!selectedReport || selectedCameras.length === 0) {
      alert('Please select a report and at least one camera');
      return;
    }

    setIsSearching(true);
    try {
      const response = await searchAPI.startSearch(selectedReport.id, selectedCameras);
      setSearchJob(response.data);
      
      // Poll for job completion
      const checkStatus = setInterval(async () => {
        const jobStatus = await searchAPI.getSearchJob(response.data.id);
        setSearchJob(jobStatus.data);
        
        if (jobStatus.data.status === 'completed' || jobStatus.data.status === 'failed') {
          clearInterval(checkStatus);
          setIsSearching(false);
        }
      }, 2000);
    } catch (err) {
      alert('Error starting search: ' + (err.response?.data?.detail || err.message));
      setIsSearching(false);
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>🔍 Search Center</h1>
      
      {/* Notification Banner */}
      {newReportLocation && (
        <div style={{ 
          backgroundColor: '#fee', 
          border: '2px solid #f00', 
          padding: '1rem', 
          marginBottom: '1rem',
          borderRadius: '8px',
          animation: 'pulse 1s infinite'
        }}>
          <strong>🔔 NEW REPORT!</strong> Last seen at location ID: {newReportLocation}
        </div>
      )}

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
      `}</style>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr 1fr', gap: '2rem', marginBottom: '2rem' }}>
        {/* Reports List */}
        <div style={{ border: '1px solid #ddd', padding: '1rem', borderRadius: '8px' }}>
          <h3>📋 Recent Reports</h3>
          <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
            {reports.map(report => (
              <div
                key={report.id}
                onClick={() => setSelectedReport(report)}
                style={{
                  padding: '0.75rem',
                  marginBottom: '0.5rem',
                  backgroundColor: selectedReport?.id === report.id ? '#e3f2fd' : '#f5f5f5',
                  border: selectedReport?.id === report.id ? '2px solid #2196f3' : '1px solid #ddd',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                <strong>{report.missing_person_name}</strong>
                <p style={{ margin: '0.25rem 0', fontSize: '0.9em' }}>
                  📍 Location: {report.location_name}
                </p>
                <p style={{ margin: '0.25rem 0', fontSize: '0.85em', color: '#666' }}>
                  Status: {report.status}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Map and Cameras */}
        <div>
          <div style={{ border: '1px solid #ddd', padding: '1rem', borderRadius: '8px', marginBottom: '1rem' }}>
            <h3>🗺️ Locations</h3>
            <AdminMap 
              onLocationSelect={setSelectedLocation} 
              blinkingLocationId={newReportLocation}
            />
          </div>
          
          <div style={{ border: '1px solid #ddd', padding: '1rem', borderRadius: '8px' }}>
            <h3>📹 Cameras in {selectedLocation?.name || 'Select a location'}</h3>
            {selectedLocation ? (
              <CameraSelector 
                locationId={selectedLocation.id} 
                onCamerasSelect={setSelectedCameras}
              />
            ) : (
              <p>Select a location from the map</p>
            )}
          </div>
        </div>

        {/* Search Controls */}
        <div style={{ border: '1px solid #ddd', padding: '1rem', borderRadius: '8px' }}>
          <h3>🔎 Search Controls</h3>
          
          {selectedReport && (
            <div style={{ marginBottom: '1rem' }}>
              <strong>Selected Report:</strong>
              <p style={{ fontSize: '0.9em' }}>{selectedReport.missing_person_name}</p>
              {selectedReport.missing_person_photo && (
                <img 
                  src={selectedReport.missing_person_photo} 
                  alt="Missing person" 
                  style={{ maxWidth: '100%', borderRadius: '4px', marginBottom: '1rem' }}
                />
              )}
            </div>
          )}

          <div style={{ marginBottom: '1rem' }}>
            <strong>Selected Cameras:</strong>
            <p style={{ fontSize: '0.9em' }}>{selectedCameras.length} camera(s)</p>
          </div>

          <button
            onClick={handleStartSearch}
            disabled={isSearching || !selectedReport || selectedCameras.length === 0}
            style={{
              width: '100%',
              padding: '0.75rem',
              backgroundColor: isSearching ? '#ccc' : '#4CAF50',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: isSearching ? 'not-allowed' : 'pointer',
              fontSize: '1em',
              fontWeight: 'bold'
            }}
          >
            {isSearching ? '⏳ Searching...' : '🚀 Start Search'}
          </button>

          {isSearching && searchJob && (
            <SearchProgress job={searchJob} />
          )}
        </div>
      </div>
    </div>
  );
}

export default AdminDashboard;
