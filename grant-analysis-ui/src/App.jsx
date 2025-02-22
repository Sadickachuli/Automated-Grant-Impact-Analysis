import { useState } from "react";
import "./App.css";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer
} from "recharts";

function App() {
  const [page, setPage] = useState("home");
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showPopup, setShowPopup] = useState(false);
  const [showResults, setShowResults] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async () => {
    if (!file) return;
    
    setLoading(true);
    setShowPopup(false);
    setShowResults(false);
    
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setAnalysis(data);
      setShowPopup(true);
    } catch (error) {
      console.error("Error during analysis:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      {/* === Navbar === */}
      <nav className="navbar">
        <div className="logo">GrantAnalyzer</div>
        <div className="nav-links">
          <span onClick={() => setPage("home")}>Home</span>
          <span onClick={() => setPage("analyze")}>Analyze</span>
        </div>
      </nav>

      {/* === Homepage === */}
      {page === "home" && (
        <div className="home">
          <h1>Welcome to Grant Report Analysis</h1>
          <p>
            Upload a grant report, and our AI will analyze key themes, sentiment, and impact areas.
          </p>
          <p><strong>How to Read the Results:</strong></p>
          <ul>
            <li>📊 <strong>Key Themes:</strong> A bar chart shows the most discussed topics.</li>
            <li>🌍 <strong>Impact Areas:</strong> Highlights organizations and sectors affected.</li>
            <li>😊 <strong>Sentiment Analysis:</strong> Measures positive or negative tones.</li>
          </ul>
          <button className="get-started-btn" onClick={() => setPage("analyze")}>
            Get Started
          </button>
        </div>
      )}

      {/* === Analysis Page === */}
      {page === "analyze" && (
        <div className="analyze">
          <h1>Grant Report Analysis</h1>
          <label className="file-upload">
            <input type="file" accept=".pdf" onChange={handleFileChange} />
            Choose File
          </label>
          {file && <p className="file-name">{file.name}</p>}
          <button onClick={handleSubmit} className="analyze-btn">Analyze</button>

          {/* === Loader === */}
          {loading && (
            <div className="loader-container">
              <div className="loader"></div>
              <p>Analyzing document...</p>
            </div>
          )}

          {/* === Pop-up Notification === */}
          {showPopup && (
            <div className="popup">
              <p>Analysis Complete</p>
              <button onClick={() => setShowResults(true)}>Tap to Show Analysis</button>
            </div>
          )}

          {/* === Results Section === */}
          {showResults && analysis && (
            <div className="results">
              <h2>Key Themes (Bar Chart)</h2>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart 
                  data={analysis.key_themes.map(([theme, count]) => ({ theme, count }))}
                >
                  <XAxis dataKey="theme" tick={{ fontSize: 10 }} />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="count" fill="#3498db" />
                </BarChart>
              </ResponsiveContainer>

              <h2>Impact Areas</h2>
              <ul>
                {analysis.impact_areas.map(([entity, label], index) => (
                  <li key={index}>
                    <strong>{entity}</strong> ({label})
                  </li>
                ))}
              </ul>

              <h2>Sentiment Analysis</h2>
              <div>
                <p>
                  <strong>Label:</strong> {analysis.sentiment[0].label}
                </p>
                <p>
                  <strong>Score:</strong> {analysis.sentiment[0].score.toFixed(2)}
                </p>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
