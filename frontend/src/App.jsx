import { useState } from "react";
import "./App.css";

export default function App() {
  const [file, setFile] = useState(null);
  const [uploaded, setUploaded] = useState(false);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");

  const BACKEND_URL = "https://rag-doc-q-a.onrender.com";

  // 🔹 HARD RESET (prevents backend context mixing)
  const resetAll = () => {
    window.location.reload();
  };

  // 🔹 Upload file
  const uploadFile = async () => {
    if (!file) return;

    setLoading(true);
    setStatus("Uploading...");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${BACKEND_URL}/files/upload`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error(`Upload failed: ${res.status}`);
      }

      // backend may or may not return JSON
      try {
        await res.json();
      } catch (_) {}

      setUploaded(true);
      setStatus("Uploaded ✓");
    } catch (err) {
      console.error(err);
      setStatus("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  // 🔹 Ask question (with timeout safety)
  const askQuestion = async () => {
    if (!uploaded || !question.trim()) return;

    setLoading(true);
    setStatus("Thinking...");
    setAnswer("");

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 60000); // 60s timeout

    try {
      const res = await fetch(`${BACKEND_URL}/chat/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
        signal: controller.signal,
      });

      if (!res.ok) {
        throw new Error(`Ask failed: ${res.status}`);
      }

      const data = await res.json();
      setAnswer(data.answer || "No answer found");
      setStatus("");
    } catch (err) {
      console.error(err);
      setStatus(
        err.name === "AbortError"
          ? "Request timed out"
          : "Failed to get answer"
      );
    } finally {
      clearTimeout(timeoutId);
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <h1 className="title">RAG Doc Q&amp;A</h1>

      <div className="card">
        {/* File Picker */}
        <label className={`file-picker ${file ? "selected" : ""}`}>
          <input
            type="file"
            accept=".pdf,.mp3,.mp4"
            onChange={(e) => setFile(e.target.files[0])}
          />
          {file ? file.name : "Choose PDF / MP3 / MP4"}
        </label>

        {/* Reset */}
        {file && (
          <button className="secondary" onClick={resetAll}>
            Reset
          </button>
        )}

        {/* Upload */}
        <button onClick={uploadFile} disabled={!file || loading}>
          {loading && !uploaded ? "Uploading..." : "Upload"}
        </button>

        {/* Question */}
        <textarea
          placeholder="Ask a question from the uploaded content..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          disabled={!uploaded}
        />

        {/* Ask */}
        <button
          className="ask"
          onClick={askQuestion}
          disabled={!uploaded || loading}
        >
          {loading && uploaded ? "Thinking..." : "Ask"}
        </button>

        {/* Status */}
        {status && <div className="status">{status}</div>}

        {/* Answer */}
        {answer && (
          <div className="answer">
            <strong>Answer</strong>
            <p>{answer}</p>
          </div>
        )}
      </div>
    </div>
  );
}
