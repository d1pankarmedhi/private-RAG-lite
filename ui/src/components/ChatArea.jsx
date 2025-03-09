import React from "react";

function ChatArea({ chatHistory }) {
  return (
    <div className="p-6 rounded-xl bg-gray-50 shadow-md overflow-y-auto h-[calc(100vh-550px)] dark:bg-gray-800 dark:shadow-none">
      <div className="space-y-5">
        {chatHistory.map((message, index) => (
          <div
            key={index}
            className={`flex ${
              message.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`rounded-xl p-4 max-w-2xl ${
                message.role === "user"
                  ? "bg-blue-100 text-gray-800"
                  : "bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-white"
              }`}
            >
              <p className="text-sm whitespace-pre-line">{message.content}</p>
            </div>
          </div>
        ))}
        {chatHistory.length === 0 && (
          <div className="text-center text-gray-400 mt-8">
            No messages yet. Ask me anything!
          </div>
        )}
      </div>
    </div>
  );
}

export default ChatArea;
