import React, { useState } from "react";

function InputArea({ onSendMessage }) {
  const [message, setMessage] = useState("");

  const handleInputChange = (e) => {
    setMessage(e.target.value);
  };

  const handleSend = () => {
    if (message.trim()) {
      onSendMessage(message);
      setMessage("");
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="mt-6">
      <textarea
        className="w-full p-4 border-gray-200 rounded-xl shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        placeholder="Ask me anything..."
        rows="4"
        value={message}
        onChange={handleInputChange}
        onKeyDown={handleKeyDown}
      />
      <button
        className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-4 rounded-xl shadow-md mt-4 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 dark:bg-blue-400 dark:hover:bg-blue-500 dark:focus:ring-blue-800"
        onClick={handleSend}
      >
        Send
      </button>
    </div>
  );
}

export default InputArea;
