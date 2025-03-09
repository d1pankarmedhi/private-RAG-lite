import React, { useState, useEffect, useRef } from "react";
import ChatArea from "./components/ChatArea";
import InputArea from "./components/InputArea";
import UploadArea from "./components/UploadArea";

function App() {
  const [chatHistory, setChatHistory] = useState([]);
  const chatAreaRef = useRef(null);

  useEffect(() => {
    if (chatAreaRef.current) {
      chatAreaRef.current.scrollTop = chatAreaRef.current.scrollHeight;
    }
  }, [chatHistory]);

  const handleSendMessage = async (message) => {
    const newUserMessage = { role: "user", content: message };
    setChatHistory((currentHistory) => [...currentHistory, newUserMessage]);

    try {
      const response = await fetch("http://localhost:8000/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: message }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const botResponse = { role: "assistant", content: data.response };
      setChatHistory((currentHistory) => [...currentHistory, botResponse]);
    } catch (error) {
      console.error("Error sending message:", error);
      const errorBotResponse = {
        role: "assistant",
        content:
          "Sorry, I couldn't process your request. Please try again later.",
      };
      setChatHistory((currentHistory) => [...currentHistory, errorBotResponse]);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-white">
      <header className="bg-blue-700 dark:bg-blue-900 p-6 text-white text-center font-semibold text-xl shadow-md">
        Phi-3 RAG Chatbot
      </header>
      <div className="flex flex-row flex-1 p-6 space-x-8 max-w-7xl mx-auto">
        <div className="w-1/3">
          <UploadArea />
        </div>
        <div className="flex-1 flex flex-col">
          <ChatArea chatHistory={chatHistory} />
          <InputArea onSendMessage={handleSendMessage} />
        </div>
      </div>
      <footer className="bg-gray-200 dark:bg-gray-800 p-4 text-center text-gray-600 dark:text-gray-400 text-sm">
        Powered by FastAPI, Phi-3, ChromaDB, and ReactJS with Tailwind CSS
      </footer>
    </div>
  );
}

export default App;
