"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

export default function ResultsPage() {
  const { jobId } = useParams();
  const [files, setFiles] = useState([]);

  useEffect(() => {
    const fetchResults = async () => {
      const res = await fetch(`http://localhost:5000/progress/${jobId}`);
      const data = await res.json();
      if (data.status === "done") {
        setFiles(data.files || []);
      }
    };
    fetchResults();
  }, [jobId]);

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8 text-center">
      <h1 className="text-3xl font-bold mb-8">Separated Stems</h1>
      {files.length ? (
        <div className="space-y-6">
          {files.map((file) => (
            <div key={file} className="bg-gray-800 rounded-xl p-4 shadow">
              <p>{file}</p>
              <audio controls src={`http://localhost:5000/results/${jobId}/${file}`} className="w-full mt-2" />
              <a
                href={`http://localhost:5000/results/${jobId}/${file}`}
                className="block mt-2 text-amber-400 hover:underline"
                download
              >
                Download
              </a>
            </div>
          ))}
          <a
            href={`http://localhost:5000/results/${jobId}/zip`}
            className="inline-block bg-amber-500 text-black px-6 py-2 rounded-lg font-semibold hover:bg-amber-600 mt-6"
            download
          >
            Download All (ZIP)
          </a>
        </div>
      ) : (
        <p>Processing your file...</p>
      )}
    </div>
  );
}
