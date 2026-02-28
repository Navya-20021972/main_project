import React, { useState } from 'react';
import '../App.css';
import ReportForm from '../components/ReportForm';

function ReportPage() {
  return (
    <div className="container">
      <div className="card">
        <h2>File Missing Person Report</h2>
        <ReportForm />
      </div>
    </div>
  );
}

export default ReportPage;
