import { useState, useEffect } from "react";

export default function DocumentList({ apiBase, refreshKey }) {
  const [docs, setDocs] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetch(`${apiBase}/documents`)
      .then((r) => r.json())
      .then((data) => setDocs(data))
      .catch(() => setDocs([]))
      .finally(() => setLoading(false));
  }, [apiBase, refreshKey]);

  const formatSize = (bytes) => {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / (1024 * 1024)).toFixed(1) + " MB";
  };

  return (
    <div className="document-list">
      <h2>Documents</h2>
      {loading && <p>Loading...</p>}
      {!loading && docs.length === 0 && <p className="empty">No documents yet</p>}
      <ul>
        {docs.map((doc) => (
          <li key={doc.name}>
            <span className="doc-name">{doc.name}</span>
            <span className="doc-size">{formatSize(doc.size)}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
