"use client";
import { useState } from "react";
import FileUploader from "@/components/FileUploader";
import LoadingIndicator from "@/components/LoadingIndicator";

export default function Home() {
  const [file, setFile] = useState(null);
  const [stems, setStems] = useState("2");
  const [quality, setQuality] = useState("standard");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!file) return alert("Please upload a file first.");
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("stems", stems);
      formData.append("quality", quality);

      const res = await fetch("http://localhost:5000/api/separate", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Server error");

      const { jobId } = await res.json();
      window.location.href = `/results/${jobId}`;
    } catch (err) {
      alert("Error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingIndicator />;

  return (
    <div className="min-h-screen bg-amber-500 text-gray-100 flex flex-col">
      {/* Navbar */}
      <nav className="flex items-center justify-between px-6 py-4 bg-gray-900 shadow-lg">
        <div className="text-2xl font-bold text-amber-500">AudioSplit</div>
        <div className="hidden md:flex gap-6">
          <a href="#features" className="hover:text-amber-400">Features</a>
          <a href="#how-it-works" className="hover:text-amber-400">How It Works</a>
          <a href="#cta" className="hover:text-amber-400">Get Started</a>
        </div>
        <button className="bg-amber-500 text-black px-4 py-2 rounded-lg hover:bg-amber-600 transition">
          Try Now
        </button>
      </nav>

      {/* Hero Section */}
      <section className="flex flex-col items-center justify-center text-center py-16 px-6 bg-gray-900 rounded-b-3xl">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          🎶 Separate Vocals & Instruments Instantly
        </h1>
        <p className="text-gray-400 max-w-2xl mb-8">
          Upload any song and get clean stems for vocals, drums, bass, and more.
          Perfect for producers, DJs, and karaoke lovers.
        </p>

        <div className="w-full max-w-md bg-gray-800 rounded-2xl p-6 shadow-xl">
          <FileUploader onFileSelect={setFile} />

          <div className="mt-6 space-y-4">
            <select
              value={stems}
              onChange={(e) => setStems(e.target.value)}
              className="w-full bg-gray-700 border border-gray-600 text-white rounded-lg px-3 py-2 focus:border-amber-500"
            >
              <option value="2">2 Stems (Vocals + Accompaniment)</option>
              <option value="4">4 Stems</option>
              <option value="5">5 Stems</option>
            </select>

            <select
              value={quality}
              onChange={(e) => setQuality(e.target.value)}
              className="w-full bg-gray-700 border border-gray-600 text-white rounded-lg px-3 py-2 focus:border-amber-500"
            >
              <option value="standard">Standard</option>
              <option value="high">High</option>
            </select>
          </div>

          <button
            onClick={handleSubmit}
            className="mt-6 w-full bg-amber-500 hover:bg-amber-600 text-black py-3 rounded-xl font-semibold shadow-md transition"
          >
            Separate Now
          </button>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-16 px-6 bg-amber-500 text-gray-900">
        <h2 className="text-3xl font-bold text-center mb-10">Why Choose AudioSplit?</h2>
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <div className="bg-white rounded-xl p-6 shadow-md text-center">
            <h3 className="font-bold text-xl mb-2">🎤 Studio-Quality Stems</h3>
            <p className="text-gray-700">Powered by AI to give you professional-grade separation.</p>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-md text-center">
            <h3 className="font-bold text-xl mb-2">⚡ Fast & Easy</h3>
            <p className="text-gray-700">Upload and get results in minutes — no software needed.</p>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-md text-center">
            <h3 className="font-bold text-xl mb-2">💻 Works Anywhere</h3>
            <p className="text-gray-700">Use it on desktop, tablet, or mobile seamlessly.</p>
          </div>
        </div>
      </section>

      {/* How it Works */}
      <section id="how-it-works" className="py-16 px-6 bg-gray-900 text-white">
        <h2 className="text-3xl font-bold text-center mb-10">How It Works</h2>
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto text-center">
          <div>
            <div className="text-5xl mb-4">⬆️</div>
            <h3 className="font-bold">1. Upload</h3>
            <p className="text-gray-400">Choose your audio or video file.</p>
          </div>
          <div>
            <div className="text-5xl mb-4">⚙️</div>
            <h3 className="font-bold">2. Process</h3>
            <p className="text-gray-400">Our AI separates the stems quickly.</p>
          </div>
          <div>
            <div className="text-5xl mb-4">⬇️</div>
            <h3 className="font-bold">3. Download</h3>
            <p className="text-gray-400">Get clean stems instantly.</p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section id="cta" className="py-16 text-center bg-amber-500 text-gray-900">
        <h2 className="text-3xl font-bold mb-4">Ready to Create?</h2>
        <p className="mb-6">Start separating vocals and instruments now.</p>
        <button
          onClick={() => document.getElementById("fileInput").click()}
          className="bg-gray-900 text-amber-500 px-6 py-3 rounded-xl font-semibold hover:bg-gray-800 transition"
        >
          Try AudioSplit Free
        </button>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 py-6 text-center text-gray-500">
        <p>© {new Date().getFullYear()} AudioSplit. All rights reserved.</p>
      </footer>
    </div>
  );
}
