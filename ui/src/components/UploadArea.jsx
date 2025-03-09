import React, { useState } from "react";

function UploadArea({ onFileUpload }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [chunkSize, setChunkSize] = useState(500);
  const [chunkOverlap, setChunkOverlap] = useState(20);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleChunkSizeChange = (event) => {
    setChunkSize(parseInt(event.target.value, 10) || 100);
  };

  const handleChunkOverlapChange = (event) => {
    setChunkOverlap(parseInt(event.target.value, 10) || 10);
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
      alert("Please select a PDF file");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append(
      "upload_config",
      JSON.stringify({ chunk_size: chunkSize, chunk_overlap: chunkOverlap }),
    );

    try {
      const response = await fetch("http://localhost:8000/upload_document/", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        alert(data.message);
        setSelectedFile(null);
      } else {
        const errorData = await response.json();
        alert(`Upload failed: ${errorData.error || "Unknown error"}`);
      }
    } catch (error) {
      console.error("Upload error:", error);
      alert("Error uploading file");
    }
  };

  return (
    <div className="p-6 rounded-xl bg-gray-50 shadow-md dark:bg-gray-800 dark:shadow-none">
      <h3 className="text-lg font-semibold mb-5 text-gray-700 dark:text-gray-300">
        Upload Document
      </h3>
      <input
        type="file"
        accept=".pdf"
        onChange={handleFileChange}
        className="mb-5 dark:text-white"
      />
      <div className="mb-4">
        <label
          htmlFor="chunkSize"
          className="block text-sm font-medium text-gray-700 dark:text-gray-300"
        >
          Chunk Size
        </label>
        <input
          type="number"
          id="chunkSize"
          value={chunkSize}
          onChange={handleChunkSizeChange}
          className="mt-1 p-3 w-full border border-gray-200 rounded-xl shadow-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-500 dark:focus:border-blue-500 shadow-sm"
          min="100"
          max="2000"
          step="100"
        />
      </div>
      <div className="mb-6">
        <label
          htmlFor="chunkOverlap"
          className="block text-sm font-medium text-gray-700 dark:text-gray-300"
        >
          Chunk Overlap
        </label>
        <input
          type="number"
          id="chunkOverlap"
          value={chunkOverlap}
          onChange={handleChunkOverlapChange}
          className="mt-1 p-3 w-full border border-gray-200 rounded-xl shadow-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-500 dark:focus:border-blue-500 shadow-sm"
          min="10"
          max="500"
          step="10"
        />
      </div>
      <button
        onClick={handleSubmit}
        className="w-full bg-green-500 hover:bg-green-600 text-white font-bold py-4 rounded-xl shadow-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50 dark:bg-green-400 dark:hover:bg-green-500 dark:focus:ring-green-800"
      >
        Upload PDF
      </button>
    </div>
  );
}

export default UploadArea;
