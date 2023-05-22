// Navbar.js or Navbar.tsx

import React from 'react';
import { Link } from 'react-router-dom';
import "./style.css"; // Import the Languages CSS file
import LoginComponent from './LoginComponent';

function Navbar() {
  return (
    <nav className="navbar">
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/authors">Authors</Link>
        </li>
        <li>
          <Link to="/books">Books</Link>
        </li>
        <li>
          <Link to="/genre">Genres</Link>
        </li>
        {/* <li>
          <Link to="/login">Login</Link>
        </li> */}
        <li>
          <Link to="/signup">Signup</Link>
        </li>
        <li>
          <Link to="/Language">Language</Link>
        </li>
        <li>
          <LoginComponent/>
        </li>        
      </ul>
    </nav>
  );
}

export default Navbar;
