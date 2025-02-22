import React from "react";
import "./App.css";

const Home = ({ setPage }) => {
  return (
    <div className="home-container">
      <div className="home">
        <h1>Grant Report Analysis</h1>
        <p>
          Upload a grant report, and our AI will analyze key themes, sentiment, and impact areas.
        </p>
        
        <button className="get-started-btn" onClick={() => setPage("analyze")}>
          Get Started
        </button>
      </div>

      {/* Background Image */}
      <img src="/images/bg3.jpg" alt="Analysis Graphic" className="background-image" />
    </div>
  );
};

export default Home;
