import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Create a separate instance for file uploads without Content-Type header
const apiForm = axios.create({
  baseURL: API_BASE_URL,
});

// Reports API
export const reportAPI = {
  createReport: (data) => apiForm.post('/reports/reports/', data),
  getReports: () => api.get('/reports/reports/'),
  getReport: (id) => api.get(`/reports/reports/${id}/`),
};

// Search API
export const searchAPI = {
  startSearch: (reportId, cameras) => apiForm.post('/search/search-jobs/start_search/', { report_id: reportId, camera_ids: cameras }),
  getSearchJob: (jobId) => api.get(`/search/search-jobs/${jobId}/`),
  getResults: (reportId) => api.get(`/reports/results/?report_id=${reportId}`),
};

// Locations API
export const locationsAPI = {
  getLocations: () => api.get('/reports/locations/'),
  getCameras: (locationId) => api.get(`/reports/cameras/?location_id=${locationId}`),
};

export default api;
