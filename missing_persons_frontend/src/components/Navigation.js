import React from 'react';
import { Link } from 'react-router-dom';

function Navigation() {
  return (
    <nav className="nav">
      <h1>🚨 Missing Persons Alert System</h1>
      <div>
        <Link to="/">File Report</Link>
        <Link to="/admin">Admin Dashboard</Link>
      </div>
    </nav>
  );
}

export default Navigation;
