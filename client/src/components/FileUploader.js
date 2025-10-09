"use client";
import { useState } from "react";

export default function FileUploader({ onFileSelect,nameText }) {
  const [dragging, setDragging] = useState(false);

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) onFileSelect(file);
  };

  return (
    <div
      className={`border-2 border-dashed rounded-xl p-8 text-center transition cursor-pointer ${
        dragging
          ? "border-amber-400 bg-gray-800"
          : "border-gray-600 bg-gray-900"
      }`}
      onDragOver={(e) => {
        e.preventDefault();
        setDragging(true);
      }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
    >
      <p className="text-gray-400">{nameText || "Drag & drop or click to upload"}</p>
      <input
        type="file"
        accept="audio/*,video/*"
        className="hidden"
        id="fileInput"
        onChange={(e) => onFileSelect(e.target.files[0])}
      />
      <label
        htmlFor="fileInput"
        className="inline-block mt-4 bg-amber-500 hover:bg-amber-600 text-black font-semibold px-4 py-2 rounded-lg cursor-pointer"
      >
        Choose File
      </label>
    </div>
  );
}
