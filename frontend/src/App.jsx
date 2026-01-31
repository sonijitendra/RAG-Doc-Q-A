import { useState } from "react";
import "./App.css";

export default function App() {
  const [file, setFile] = useState(null);
  const [uploaded, setUploaded] = useState(false);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");

  // Reset everything
  const resetAll = () => {
    setFile(null);
    setUploaded(false);
    setQuestion("");
    setAnswer("");
    setStatus("");
  };

  // Upload file
  const uploadFile = async () => {
    if (!file) return;

    setLoading(true);
    setStatus("Uploading...");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/files/upload", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error(`Upload failed with status ${res.status}`);
      }

      const data = await res.json();
      console.log("Upload response:", data);

      setUploaded(true);
      setStatus("Uploaded ✓");
    } catch (err) {
      console.error(err);
      setStatus("Upload failed");
    }

    setLoading(false);
  };

  // Ask question
  const askQuestion = async () => {
    if (!uploaded || !question.trim()) return;

    setLoading(true);
    setStatus("Thinking...");
    setAnswer("");

    try {
      const res = await fetch("http://127.0.0.1:8000/chat/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question,
        }),
      });

      if (!res.ok) {
        throw new Error(`Ask failed with status ${res.status}`);
      }

      const data = await res.json();
      setAnswer(data.answer || "No answer found");
      setStatus("");
    } catch (err) {
      console.error(err);
      setStatus("Failed to get answer");
    }

    setLoading(false);
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
            Deselect File
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
