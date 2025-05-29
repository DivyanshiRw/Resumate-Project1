import React from 'react';
import logo from './resumate-logo.jpeg';

function Navbar() {
  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-dark shadow-sm">
      <div className="container">
        <a className="navbar-brand d-flex align-items-center" href="/">
          <img src={logo} alt="Logo" width="50" height="50" className="me-2 rounded-pill"/>
          <span className="fw-bold fs-5 text-white">ResuMate</span>
        </a>
      </div>
    </nav>
  );
}

export default Navbar;
