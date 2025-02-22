import React from "react";
import "./App.css";

const Navbar = ({ setPage }) => {
  return (
    <nav className="navbar">
      <div className="logo">GrantAI</div>
      <div className="nav-links">
        <button onClick={() => setPage("home")}>Home</button>
        <button onClick={() => setPage("analyze")}>Analyze</button>
      </div>
    </nav>
  );
};

export default Navbar;
