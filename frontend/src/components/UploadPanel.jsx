import { useState, useRef } from "react";

export default function UploadPanel({ apiBase, onUploaded }) {
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");
  const [dragOver, setDragOver] = useState(false);
  const fileInput = useRef(null);

  const uploadFile = async (file) => {
    if (!file || !file.name.toLowerCase().endsWith(".pdf")) {
      setMessage("Please select a PDF file.");
      return;
    }
    setUploading(true);
    setMessage("");
    try {
      const formData = new FormData();
      formData.append("file", file);
      const res = await fetch(`${apiBase}/upload`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (!res.ok) {
        setMessage("Error: " + (data.message || data.detail || "Upload failed"));
        return;
      }
      setMessage(data.message);
      onUploaded();
    } catch (err) {
      setMessage("Upload failed: " + err.message);
    } finally {
      setUploading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    uploadFile(file);
  };

  return (
    <div className="upload-panel">
      <h2>Upload PDF</h2>
      <div
        className={`drop-zone ${dragOver ? "drag-over" : ""}`}
        onDragOver={(e) => {
          e.preventDefault();
          setDragOver(true);
        }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        onClick={() => fileInput.current?.click()}
      >
        {uploading ? "Uploading..." : "Drop PDF here or click to browse"}
      </div>
      <input
        ref={fileInput}
        type="file"
        accept=".pdf"
        style={{ display: "none" }}
        onChange={(e) => uploadFile(e.target.files[0])}
      />
      {message && <p className="upload-message">{message}</p>}
    </div>
  );
}
