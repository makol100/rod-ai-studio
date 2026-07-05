import { useState } from "react";
import "./App.css";

const API_URL = "http://157.90.155.155:8000/generate-reel";

export default function App() {
  const [prompt, setPrompt] = useState("");
  const [status, setStatus] = useState("");
  const [result, setResult] = useState(null);

  async function generateReel() {
    if (!prompt.trim()) {
      setStatus("Wpisz temat rolki.");
      return;
    }

    setStatus("Generuję rolkę...");
    setResult(null);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) {
        throw new Error("Błąd API: " + response.status);
      }

      const data = await response.json();
      setResult(data);
      setStatus("Gotowe.");
    } catch (error) {
      setStatus("Błąd: " + error.message);
    }
  }

  return (
    <main style={{ maxWidth: 700, margin: "40px auto", padding: 20, fontFamily: "Arial, sans-serif" }}>
      <h1>ROD AI Studio</h1>
      <p>Generator rolek dla ogrodu.</p>

      <textarea
        rows={6}
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Np. 12 najczęstszych błędów podczas uprawy pomidorów"
        style={{ width: "100%", fontSize: 16, padding: 12, boxSizing: "border-box" }}
      />

      <br /><br />

      <button onClick={generateReel} style={{ width: "100%", padding: 16, fontSize: 18 }}>
        Generuj rolkę
      </button>

      {status && <p><strong>{status}</strong></p>}

      {result && (
        <pre style={{ whiteSpace: "pre-wrap", background: "#222", padding: 12 }}>
{JSON.stringify(result, null, 2)}
        </pre>
      )}
    </main>
  );
}
