"use client";

import { useState } from "react";

export default function Home() {

  const [name, setName] = useState("");
  const [image, setImage] = useState<File | null>(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [scannerActive, setScannerActive] = useState(false);

  // Register Student
  const registerStudent = async () => {

    if (!name || !image) {

      alert("Enter student name and select image");

      return;
    }

    const formData = new FormData();

    formData.append("name", name);
    formData.append("image", image);

    try {

      setLoading(true);

      const response = await fetch(
        "http://127.0.0.1:8000/register",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      setMessage(data.message);

      setName("");

    } catch (error) {

      console.error(error);

      setMessage("Registration failed");

    } finally {

      setLoading(false);
    }
  };

  // Start Scanner
  const startScanning = async () => {

    alert(
      "AiTendance Scanner Starting...\n\nPress Q to finish attendance."
    );

    try {

      setScannerActive(true);

      await fetch(
        "http://127.0.0.1:8000/scan"
      );

    } catch (error) {

      console.error(error);

    } finally {

      setScannerActive(false);
    }
  };

  // Download Excel
  const downloadAttendance = () => {

    window.open(
      "http://127.0.0.1:8000/download-attendance",
      "_blank"
    );
  };

  return (

    <main className="min-h-screen bg-gradient-to-br from-black via-zinc-900 to-black text-white p-8">

      <div className="max-w-7xl mx-auto">

        {/* Header */}
        <div className="flex justify-between items-center mb-12">

          <div>

            <h1 className="text-7xl font-black text-green-400">
              AiTendance
            </h1>

            <p className="text-gray-400 mt-2 text-lg">
              AI Powered Smart Classroom Attendance
            </p>

          </div>

          <div className="bg-zinc-900 border border-green-500 px-6 py-3 rounded-2xl shadow-lg">

            <p className="text-green-400 font-bold text-lg">
              LIVE AI SYSTEM
            </p>

          </div>

        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

          {/* Register Student */}
          <div className="bg-zinc-900 border border-zinc-800 rounded-3xl p-8 shadow-2xl">

            <h2 className="text-4xl font-bold mb-8">
              Register Student
            </h2>

            <input
              type="text"
              placeholder="Enter Student Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full p-4 rounded-xl bg-black border border-zinc-700 mb-5 text-lg"
            />

            <input
              type="file"
              accept="image/*"
              onChange={(e) => {

                if (e.target.files) {
                  setImage(e.target.files[0]);
                }

              }}
              className="w-full mb-8"
            />

            <button
              onClick={registerStudent}
              disabled={loading}
              className="w-full bg-green-500 hover:bg-green-600 transition-all p-4 rounded-xl font-bold text-xl"
            >

              {
                loading
                  ? "Processing..."
                  : "Register Student"
              }

            </button>

            {message && (

              <div className="mt-6 bg-black border border-green-500 p-4 rounded-xl">

                <p className="text-green-400 text-center text-lg">
                  {message}
                </p>

              </div>

            )}

          </div>

          {/* Scanner */}
          <div className="bg-zinc-900 border border-zinc-800 rounded-3xl p-8 shadow-2xl">

            <h2 className="text-4xl font-bold mb-8">
              Classroom Scanner
            </h2>

            {/* Scanner Display */}
            <div className="bg-black rounded-2xl h-72 flex flex-col items-center justify-center border border-zinc-700 mb-8 relative overflow-hidden">

              {
                scannerActive ? (

                  <>
                    <div className="absolute inset-0 border-4 border-green-500 animate-pulse rounded-2xl"></div>

                    <p className="text-7xl mb-4">
                      🎥
                    </p>

                    <p className="text-green-400 text-2xl font-bold">
                      AI Scanner Running...
                    </p>

                    <p className="text-gray-400 mt-2">
                      OpenCV Classroom Detection Active
                    </p>
                  </>

                ) : (

                  <>
                    <p className="text-7xl mb-4">
                      🎥
                    </p>

                    <p className="text-gray-400 text-lg">
                      AI Multi Face Detection Active
                    </p>
                  </>

                )
              }

            </div>

            {/* Start Scanner */}
            <button
              onClick={startScanning}
              disabled={loading}
              className="w-full bg-blue-500 hover:bg-blue-600 transition-all p-4 rounded-xl font-bold text-xl mb-4"
            >

              {
                scannerActive
                  ? "Scanner Running..."
                  : "Start Classroom Attendance"
              }

            </button>

            {/* Download Excel */}
            <button
              onClick={downloadAttendance}
              className="w-full bg-green-500 hover:bg-green-600 transition-all p-4 rounded-xl font-bold text-xl"
            >
              Download Attendance Excel
            </button>

            {/* Status Cards */}
            <div className="mt-8 grid grid-cols-2 gap-4">

              <div className="bg-black p-5 rounded-xl border border-zinc-700">

                <p className="text-gray-400 text-sm">
                  Face Detection
                </p>

                <p className="text-green-400 font-bold text-2xl">
                  ACTIVE
                </p>

              </div>

              <div className="bg-black p-5 rounded-xl border border-zinc-700">

                <p className="text-gray-400 text-sm">
                  Attendance
                </p>

                <p className="text-green-400 font-bold text-2xl">
                  LIVE
                </p>

              </div>

            </div>

          </div>

        </div>

      </div>

    </main>
  );
}