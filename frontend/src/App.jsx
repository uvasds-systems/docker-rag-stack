import { useState } from "react";
import ChatWindow from "./components/ChatWindow";
import DocumentList from "./components/DocumentList";
import UploadPanel from "./components/UploadPanel";

const API_BASE = "/api";

export default function App() {
  const [refreshDocs, setRefreshDocs] = useState(0);

  const onUploaded = () => setRefreshDocs((r) => r + 1);

  return (
    <div className="app">
      <header>
        <h1>RAG Document Chat</h1>
      </header>
      <div className="main-layout">
        <aside className="sidebar">
          <UploadPanel apiBase={API_BASE} onUploaded={onUploaded} />
          <DocumentList apiBase={API_BASE} refreshKey={refreshDocs} />
        </aside>
        <main className="chat-area">
          <ChatWindow apiBase={API_BASE} />
        </main>
      </div>
    </div>
  );
}
