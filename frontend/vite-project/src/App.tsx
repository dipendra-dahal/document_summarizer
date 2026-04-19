import { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

const ALLOWED_TYPES = ["application/pdf", "text/plain"];
const MAX_FILE_SIZE_MB = 10;

function App() {
  const [length, setLength] = useState("short");
  const [file, setFile] = useState<File | null>(null);
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [truncated, setTruncated] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0] || null;
    setFile(selected);
    setError("");
    setSummary("");
    setTruncated(false);
  };

  const handleSubmit = async () => {
    setError("");
    setSummary("");
    setTruncated(false);

    if (!file) {
      setError("Please upload a file.");
      return;
    }

    if (!ALLOWED_TYPES.includes(file.type)) {
      setError("Only PDF or TXT allowed.");
      return;
    }

    if (file.size > MAX_FILE_SIZE_MB * 1024 * 1024) {
      setError("File too large (max 10MB).");
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("length", length);
      formData.append("focus", "key points"); 

      const res = await fetch(`${API_URL}/summarize`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data?.detail || "Request failed");
      }

      setSummary(data.summary);
      setTruncated(data.truncated ?? false);

    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20, maxWidth: 800, margin: "auto" }}>
      <h1> Document Summarizer</h1>

      <input type="file" accept=".pdf,.txt" onChange={handleFileChange} />

      {file && <p>📎 {file.name}</p>}

      <br />

      <label>Summary Length: </label>
      <select value={length} onChange={(e) => setLength(e.target.value)}>
        <option value="short">Short</option>
        <option value="medium">Medium</option>
        <option value="long">Long</option>
      </select>

      <br /><br />

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Summarizing..." : "Generate Summary"}
      </button>

      {error && <p style={{ color: "red" }}>⚠️ {error}</p>}

      <hr />

      {summary && (
        <div>
          <h2>Summary</h2>

          {truncated && (
            <p style={{ color: "orange" }}>
              Text was truncated to 12,000 characters
            </p>
          )}

          <pre style={{ whiteSpace: "pre-wrap" }}>
            {summary}
          </pre>
        </div>
      )}
    </div>
  );
}

export default App;