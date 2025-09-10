"use client";

export default function StemPlayer({ name, url }) {
  return (
    <div className="bg-gray-800 rounded-xl p-4 flex items-center justify-between hover:bg-gray-700 transition">
      <span className="font-medium text-white">{name}</span>
      <div className="flex items-center gap-4">
        <audio controls src={url} className="w-48 bg-gray-900 rounded-md" />
        <a
          href={url}
          download
          className="bg-amber-500 hover:bg-amber-600 text-black px-3 py-1 rounded-lg font-semibold shadow-sm transition"
        >
          Download
        </a>
      </div>
    </div>
  );
}
