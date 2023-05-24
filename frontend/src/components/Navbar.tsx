// Navbar.js or Navbar.tsx

import React from "react";
import { Link } from "react-router-dom";
import "./style.css"; // Import the Languages CSS file
import LoginComponent from "./LoginComponent";

function Navbar() {
  return (
    <nav className="navbar">
      <ul style={{ justifyContent: "space-between" }}>
        <div style={{ flexDirection: "row", display: "flex" }}>
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
          <li style={{ justifyContent: "flex-end" }}>
            <Link to="/Language">Language</Link>
          </li>
          <li style={{ justifyContent: "flex-end" }}>
            <Link to="/users">Users</Link>
          </li>
          <li>
            <Link to="/my_borrowed">My Borrowed</Link>
          </li>
        </div>

        <div style={{ flexDirection: "row", display: "flex" }}>
          <li style={{ justifyContent: "flex-end" }}>
            <Link to="/signup">Signup</Link>
          </li>
          <li>
            <LoginComponent />
          </li>
        </div>
      </ul>
    </nav>
  );
}

export default Navbar;
