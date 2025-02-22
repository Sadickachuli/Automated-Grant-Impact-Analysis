import { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async () => {
    if (!file) return;

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
    }
  };

  return (
    <div className="App">
      <h1>Grant Report Analysis</h1>
      <input type="file" accept=".pdf" onChange={handleFileChange} />
      <button onClick={handleSubmit}>Analyze</button>
      
      {analysis && (
        <div className="results">
          <h2>Key Themes</h2>
          <ul>
            {analysis.key_themes.map(([theme, count], index) => (
              <li key={index}>
                <strong>{theme}</strong>: {count}
              </li>
            ))}
          </ul>

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
  );
}

export default App;
