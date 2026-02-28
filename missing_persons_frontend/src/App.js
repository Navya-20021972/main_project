import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Navigation from './components/Navigation';
import ReportPage from './pages/ReportPage';
import AdminDashboard from './pages/AdminDashboard';
import SearchResults from './pages/SearchResults';

function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <Routes>
          <Route path="/" element={<ReportPage />} />
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/results/:reportId" element={<SearchResults />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
