import { useState, useEffect, useRef } from "react";
import axios from "axios";

// --- SVG Icons for Copy Button ---
const CopyIcon = () => (
  <svg
    width="16"
    height="16"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className="text-gray-400"
  >
    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
  </svg>
);

const CheckIcon = () => (
  <svg
    width="16"
    height="16"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="3"
    strokeLinecap="round"
    strokeLinejoin="round"
    className="text-green-400"
  >
    <polyline points="20 6 9 17 4 12"></polyline>
  </svg>
);

export default function Chat() {
  const [query, setQuery] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [fileName, setFileName] = useState("");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [copiedIndex, setCopiedIndex] = useState(null);
  const chatEndRef = useRef(null);

  // --- State to control layout ---
  const isChatStarted = chatHistory.length > 0;
  // --- State to control input bar visibility ---
  const [isDocUploaded, setIsDocUploaded] = useState(false);

  const API_BASE = "http://127.0.0.1:8000";

  const clearMessages = () => {
    setError("");
    setMessage("");
  };

  // --- Robust Copy Function ---
  const handleCopy = async (text, index) => {
    if (!text) return;
    if (navigator.clipboard && window.isSecureContext) {
      try {
        await navigator.clipboard.writeText(text);
        setCopiedIndex(index);
        setTimeout(() => setCopiedIndex(null), 2000);
        return;
      } catch (err) {
        console.warn("navigator.clipboard.writeText failed, falling back...");
      }
    }
    try {
      const textArea = document.createElement("textarea");
      textArea.value = text;
      textArea.style.position = "absolute";
      textArea.style.left = "-9999px";
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand("copy");
      document.body.removeChild(textArea);
      setCopiedIndex(index);
      setTimeout(() => setCopiedIndex(null), 2000);
    } catch (err) {
      console.error("Failed to copy text with either method:", err);
      setError("Failed to copy text. Please copy manually.");
    }
  };

  // --- Handle file upload ---
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    if (file.type !== "application/pdf") {
      setError("Please upload a PDF file only.");
      return;
    }
    setUploading(true);
    setFileName(file.name);
    clearMessages();
    try {
      const formData = new FormData();
      formData.append("file", file);
      const res = await axios.post(`${API_BASE}/upload/pdf`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMessage(res.data.message || "File uploaded successfully!");
      setIsDocUploaded(true); // Show the input bar on successful upload
    } catch (err) {
      console.error(err);
      const errorDetail = err.response?.data?.detail || "Failed to upload PDF.";
      setError(`⚠️ ${errorDetail}`);
      setIsDocUploaded(false); // Hide bar again if upload fails
    } finally {
      setUploading(false);
      event.target.value = null;
    }
  };

  // Handle chat query
  const handleSubmit = async (e) => {
    e.preventDefault();
    const userQuery = query.trim();
    if (!userQuery) return;
    setLoading(true);
    clearMessages();
    setChatHistory(prev => [...prev, { sender: 'user', text: userQuery }]);
    setQuery("");
    try {
      const res = await axios.post(`${API_BASE}/chat/query`, { query: userQuery });
      const aiResponse = res.data.response || "No response received";
      setChatHistory(prev => [...prev, { sender: 'ai', text: aiResponse }]);
    } catch (err) {
      console.error(err);
      const errorDetail = err.response?.data?.detail || "Unable to connect to the server.";
      setChatHistory(prev => [...prev, { sender: 'ai', text: `⚠️ Error: ${errorDetail}` }]);
    } finally {
      setLoading(false);
    }
  };

  // Auto-scroll effect
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatHistory]);

  return (
    // Main container is a flex column that takes full screen height
    <div className="h-screen bg-gray-900 text-white flex flex-col items-center p-6">

      {/* --- Top Section (Title, Upload) --- */}
      <div className={`w-full max-w-4xl transition-all duration-500 ease-in-out ${
          !isChatStarted 
            ? 'flex-1 flex flex-col justify-center items-center' 
            : ''
        }`}>
        
        {/* Title: Animates size */}
        <h1
        className={`text-blue-400 transition-all duration-500 ease-in-out ${
          !isChatStarted 
            ? "text-4xl font-bold mb-6" 
            : "text-2xl font-semibold mb-4"
        }`}
      >
        📄 Smart AI Document Assistant
      </h1>

        {/* --- MODIFIED: Upload Button Container --- */}
        {/* This div will be full-width after chat starts, but the button inside won't stretch */}
        <div className={`transition-all duration-500 ease-in-out ${!isChatStarted ? '' : 'w-full'}`}>
          
          {/* --- THIS IS THE FIX --- */}
          {/* I removed the conditional 'block' class to keep the button size consistent */}
          <label className={`cursor-pointer bg-blue-600 hover:bg-blue-700 px-5 py-2 rounded-lg text-center ${uploading ? 'opacity-50' : ''}`}>
            {uploading ? "Uploading..." : "📄 Upload PDF"}
            <input
              type="file"
              accept=".pdf"
              onChange={handleFileUpload}
              className="hidden"
              disabled={uploading}
            />
          </label>
          
          {fileName && (
            <p className={`text-sm text-gray-400 mt-2 ${!isChatStarted ? 'text-center' : ''}`}>
              Last Upload: {fileName}
            </p>
          )}
        </div>
        
        {/* Error/Messages: Shown here ONLY if chat hasn't started */}
        {!isChatStarted && (
          <div className="w-full max-w-lg mt-4">
            {error && (
              <div className="w-full p-3 mb-4 bg-red-800 border border-red-600 text-red-100 rounded-lg">
                {error}
              </div>
            )}
            {message && (
              <div className="w-full p-3 mb-4 bg-green-800 border border-green-600 text-green-100 rounded-lg">
                {message}
              </div>
            )}
          </div>
        )}
      </div>

      {/* --- Chat Section (Only appears AFTER chat starts) --- */}
      {isChatStarted && (
        <>
          {/* Error/Messages: Shown here ONLY if chat HAS started */}
          <div className="w-full max-w-4xl">
            {error && (
              <div className="w-full p-3 mb-4 bg-red-800 border border-red-600 text-red-100 rounded-lg">
                {error}
              </div>
            )}
            {message && (
              <div className="w-full p-3 mb-4 bg-green-800 border border-green-600 text-green-100 rounded-lg">
                {message}
              </div>
            )}
          </div>

          {/* Chat History Box */}
          <div className="flex-1 w-full max-w-4xl overflow-y-auto bg-gray-800 rounded-t-lg p-4 space-y-4">
            {chatHistory.map((msg, index) => (
              <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`relative max-w-lg p-3 rounded-lg ${msg.sender === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'}`}>
                  <p className="whitespace-pre-line pr-8">{msg.text}</p>
                  <button
                    onClick={() => handleCopy(msg.text, index)}
                    className="absolute top-2 right-2 p-1 rounded-full bg-black bg-opacity-20 hover:bg-opacity-40 transition-all"
                    title="Copy text"
                  >
                    {copiedIndex === index ? <CheckIcon /> : <CopyIcon />}
                  </button>
                </div>
              </div>
            ))}
            <div ref={chatEndRef} />
          </div>
        </>
      )}

      {/* --- Chat Input Form (Conditionally rendered) --- */}
      {/* This section will ONLY appear if isDocUploaded is true */}
      {isDocUploaded && (
        <form onSubmit={handleSubmit} className={`w-full max-w-4xl flex ${
            isChatStarted ? 'rounded-b-lg' : 'rounded-lg' // Attach to chat box or stand alone
          } overflow-hidden ${
            !isChatStarted ? 'mt-4' : '' // Add margin-top if chat hasn't started
          }`}>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask about the uploaded document..."
            className="flex-grow p-3 text-black focus:outline-none"
          />
          <button
            type="submit"
            disabled={loading || uploading}
            className="bg-blue-500 hover:bg-blue-600 px-6 py-3 disabled:opacity-50"
          >
            {loading ? (
              <span className="thinking-dots">
                <span>Thinking</span><span className="dot-1">.</span><span className="dot-2">.</span><span className="dot-3">.</span>
              </span>
            ) : (
              "Ask"
            )}
          </button>
        </form>
      )}
    </div>
  );
}