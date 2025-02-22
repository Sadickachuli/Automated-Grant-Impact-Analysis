import { useState } from "react";
import "./App.css";
import Navbar from "./Navbar";
import Home from "./Home";
import Analyze from "./Analyze";

function App() {
  const [page, setPage] = useState("home");

  return (
    <div className="App">
      <Navbar setPage={setPage} />
      {page === "home" ? <Home setPage={setPage} /> : <Analyze />}
    </div>
  );
}

export default App;
