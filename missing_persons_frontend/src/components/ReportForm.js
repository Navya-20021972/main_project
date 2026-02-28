import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';

function ReportForm() {
  const [formData, setFormData] = useState({
    missing_person_name: '',
    description: '',
    last_seen_location: '',
    last_seen_time: '',
    missing_person_photo: null
  });

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
    // TODO: Send to backend
    console.log('Submitting report:', formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="form-group">
        <label>Missing Person Name</label>
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
        <label>Photo</label>
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
        <label>Description</label>
        <textarea
          name="description"
          value={formData.description}
          onChange={handleInputChange}
          placeholder="Physical description, clothing, etc."
        />
      </div>

      <div className="form-group">
        <label>Last Seen Location</label>
        <input
          type="text"
          name="last_seen_location"
          value={formData.last_seen_location}
          onChange={handleInputChange}
          placeholder="Library, Canteen, etc."
        />
      </div>

      <div className="form-group">
        <label>Last Seen Time</label>
        <input
          type="datetime-local"
          name="last_seen_time"
          value={formData.last_seen_time}
          onChange={handleInputChange}
        />
      </div>

      <button type="submit" className="btn">Submit Report</button>
    </form>
  );
}

export default ReportForm;
