import { useState } from "react";
import "./App.css";
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer 
} from "recharts";

const Analyze = () => {
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async () => {
    if (!file) return;
    setLoading(true);
    setAnalysis(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      console.log("Response data:", data);
      setAnalysis(data);
    } catch (error) {
      console.error("Error during analysis:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="analyze-container">
      <h1>Upload a Grant Report</h1>
      <input type="file" accept=".pdf" onChange={handleFileChange} />
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze"}
      </button>

      {/* Loader */}
      {loading && <div className="loader"></div>}

      {/* Analysis Complete Pop-up */}
      {analysis && !showResults && (
        <div className="popup">
          <p>Analysis Complete!</p>
          <button onClick={() => setShowResults(true)}>Tap to Show Analysis</button>
        </div>
      )}

      {/* Show Analysis */}
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
              <Bar dataKey="count" fill="#00bfff" />
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
          <p><strong>Label:</strong> {analysis.sentiment[0].label}</p>
          <p><strong>Score:</strong> {analysis.sentiment[0].score.toFixed(2)}</p>
        </div>
      )}
    </div>
  );
};

export default Analyze;
