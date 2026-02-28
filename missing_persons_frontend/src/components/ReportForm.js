import React, { useState, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import { reportAPI, locationsAPI } from '../services/api';

function ReportForm() {
  const [formData, setFormData] = useState({
    missing_person_name: '',
    description: '',
    last_seen_location: '',
    last_seen_time: '',
    missing_person_photo: null
  });
  const [locations, setLocations] = useState([]);
  const [locationsLoading, setLocationsLoading] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  // Fetch locations on component mount
  useEffect(() => {
    const fetchLocations = async () => {
      try {
        const response = await locationsAPI.getLocations();
        setLocations(response.data.results || []);
      } catch (err) {
        console.error('Error fetching locations:', err);
        setError('Failed to load locations');
      } finally {
        setLocationsLoading(false);
      }
    };
    fetchLocations();
  }, []);

  const { getRootProps, getInputProps } = useDropzone({
    maxFiles: 1,
    accept: { 'image/*': ['.jpeg', '.jpg', '.png'] },
    onDrop: acceptedFiles => {
      if (acceptedFiles.length > 0) {
        setFormData({
          ...formData,
          missing_person_photo: acceptedFiles[0]
        });
      }
    }
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      // Create FormData for file upload
      const data = new FormData();
      data.append('missing_person_name', formData.missing_person_name);
      data.append('description', formData.description);
      data.append('last_seen_location', formData.last_seen_location);
      data.append('last_seen_time', formData.last_seen_time);
      if (formData.missing_person_photo) {
        data.append('missing_person_photo', formData.missing_person_photo);
      }

      const response = await reportAPI.createReport(data);
      
      setSuccess(true);
      // Reset form
      setFormData({
        missing_person_name: '',
        description: '',
        last_seen_location: '',
        last_seen_time: '',
        missing_person_photo: null
      });

      // Show success message
      setTimeout(() => {
        setSuccess(false);
      }, 5000);

      console.log('Report created:', response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit report. Please try again.');
      console.error('Error submitting report:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '2rem auto', padding: '2rem', border: '1px solid #ddd', borderRadius: '8px' }}>
      <h2>File Missing Person Report</h2>
      
      {error && <div style={{ backgroundColor: '#fee', color: '#c00', padding: '1rem', marginBottom: '1rem', borderRadius: '4px' }}>{error}</div>}
      {success && <div style={{ backgroundColor: '#efe', color: '#0c0', padding: '1rem', marginBottom: '1rem', borderRadius: '4px' }}>Report submitted successfully!</div>}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Missing Person Name *</label>
          <input
            type="text"
            name="missing_person_name"
            value={formData.missing_person_name}
            onChange={handleInputChange}
            required
            placeholder="Enter full name"
          />
        </div>

        <div className="form-group">
          <label>Photo *</label>
          <div {...getRootProps()} style={{ border: '2px dashed #667eea', padding: '2rem', textAlign: 'center', borderRadius: '4px', cursor: 'pointer' }}>
            <input {...getInputProps()} />
            {formData.missing_person_photo ? (
              <p>✓ {formData.missing_person_photo.name}</p>
            ) : (
              <p>Drag and drop a photo here, or click to select</p>
            )}
          </div>
        </div>

        <div className="form-group">
          <label>Description *</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleInputChange}
            required
            placeholder="Physical description, clothing, etc."
          />
        </div>

        <div className="form-group">
          <label>Last Seen Location *</label>
          {locationsLoading ? (
            <p>Loading locations...</p>
          ) : (
            <select
              name="last_seen_location"
              value={formData.last_seen_location}
              onChange={handleInputChange}
              required
              style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ccc' }}
            >
              <option value="">Select a location</option>
              {locations.map((loc) => (
                <option key={loc.id} value={loc.id}>
                  {loc.name}
                </option>
              ))}
            </select>
          )}
        </div>

        <div className="form-group">
          <label>Last Seen Time *</label>
          <input
            type="datetime-local"
            name="last_seen_time"
            value={formData.last_seen_time}
            onChange={handleInputChange}
            required
          />
        </div>

        <button type="submit" className="btn" disabled={loading} style={{ width: '100%', padding: '0.75rem', backgroundColor: '#667eea', color: 'white', border: 'none', borderRadius: '4px', cursor: loading ? 'not-allowed' : 'pointer', opacity: loading ? 0.6 : 1 }}>
          {loading ? 'Submitting...' : 'Submit Report'}
        </button>
      </form>
    </div>
  );
}

export default ReportForm;
