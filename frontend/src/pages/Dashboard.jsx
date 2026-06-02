
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const navigate = useNavigate();

  const [video, setVideo] = useState(null);
  const [prompt, setPrompt] = useState(
    "Create cinematic vertical short"
  );

  const [loading, setLoading] = useState(false);
  const [output, setOutput] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/");
    }
  }, [navigate]);

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");

    navigate("/");
  };

  const handleVideoChange = (e) => {
    const file = e.target.files[0];

    if (file) {
      setVideo(file);
      setOutput(null);
    }
  };

  const handleProcessVideo = async () => {
    if (!video) {
      alert("Please upload a video first.");
      return;
    }

    setLoading(true);

    const formData = new FormData();

    formData.append("video", video);
    formData.append("prompt", prompt);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/process-video/",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      console.log(data);

      if (!response.ok) {
        alert(
          data.error ||
          "Backend processing failed."
        );
        return;
      }

      if (data.output?.output_video) {

        setOutput(
          `http://127.0.0.1:8000/${data.output.output_video}`
        );

      } else {

        alert(
          "No output video received."
        );

      }

    } catch (error) {

      console.error(error);

      alert(
        "Server unreachable. Make sure Django is running."
      );

    } finally {

      setLoading(false);

    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-blue-950 to-black text-white px-6 py-10">

      <div className="max-w-7xl mx-auto">

        {/* Navbar */}

        <div className="flex justify-between items-center mb-10">

          <div>

            <h2 className="text-2xl font-bold">
              Welcome,
              {" "}
              {localStorage.getItem("username")}
            </h2>

            <p className="text-slate-400">
              AI Video Editing Dashboard
            </p>

          </div>

          <button
            onClick={logout}
            className="px-5 py-3 rounded-xl bg-red-600 hover:bg-red-500 transition"
          >
            Logout
          </button>

        </div>

        {/* Hero */}

        <div className="text-center mb-10">

          <h1 className="text-5xl md:text-6xl font-extrabold bg-gradient-to-r from-purple-400 via-pink-400 to-cyan-400 bg-clip-text text-transparent">
            AI Video Editor
          </h1>

          <p className="mt-4 text-slate-400 text-lg">
            Upload • Caption • Edit • Export
          </p>

        </div>

        {/* Main Layout */}

        <div className="grid lg:grid-cols-2 gap-8">

          {/* Left Side */}

          <div className="rounded-3xl border border-white/10 bg-white/5 backdrop-blur-2xl p-8 shadow-2xl">

            <label className="block mb-3 text-lg font-semibold">
              Upload Video
            </label>

            <label className="flex items-center justify-center w-full h-36 border-2 border-dashed border-purple-500/40 rounded-2xl cursor-pointer bg-slate-900/70 hover:bg-slate-800/80 transition-all">

              <div className="text-center px-4">

                <div className="text-4xl mb-2">
                  🎬
                </div>

                <p className="font-semibold text-lg">

                  {video
                    ? "Video Selected"
                    : "Upload Video"}

                </p>

                <p className="text-sm text-slate-400 mt-1">
                  Click to upload
                </p>

                {video && (

                  <p className="text-purple-300 text-sm mt-2 truncate">
                    {video.name}
                  </p>

                )}

              </div>

              <input
                type="file"
                accept="video/*"
                onChange={handleVideoChange}
                className="hidden"
              />

            </label>

            {/* Prompt */}

            <div className="mt-8">

              <label className="block mb-3 text-lg font-semibold">
                Editing Prompt
              </label>

              <textarea
                value={prompt}
                onChange={(e) =>
                  setPrompt(
                    e.target.value
                  )
                }
                rows={5}
                className="w-full bg-slate-900/70 border border-white/10 rounded-2xl p-4 focus:outline-none focus:ring-2 focus:ring-purple-500 resize-none"
              />

            </div>

            {/* Quick Prompts */}

            <div className="mt-6">

              <p className="mb-3 text-slate-300">
                Quick Prompts
              </p>

              <div className="flex flex-wrap gap-3">

                {[
                  "Create cinematic vertical short",
                  "Instagram reel style",
                  "Podcast clip",
                  "Hormozi captions",
                  "Trim to 15 seconds",
                ].map((item) => (

                  <button
                    key={item}
                    onClick={() =>
                      setPrompt(item)
                    }
                    className="px-4 py-2 rounded-full bg-slate-800 hover:bg-purple-600 transition text-sm"
                  >
                    {item}
                  </button>

                ))}

              </div>

            </div>

            {/* Generate */}

            <button
              onClick={handleProcessVideo}
              disabled={loading}
              className="mt-8 w-full py-4 rounded-2xl bg-gradient-to-r from-violet-600 to-fuchsia-600 font-bold text-lg hover:scale-[1.02] transition-all disabled:opacity-50"
            >

              {loading
                ? "🤖 Processing..."
                : "🚀 Generate Video"}

            </button>

            {loading && (

              <div className="mt-5 rounded-xl bg-slate-900/60 p-4">

                <p>
                  AI is editing your video...
                </p>

                <div className="w-full h-2 bg-slate-700 rounded-full mt-3 overflow-hidden">

                  <div className="h-full w-2/3 bg-gradient-to-r from-purple-500 to-pink-500 animate-pulse" />

                </div>

              </div>

            )}

          </div>

          {/* Right Side */}

          <div className="rounded-3xl border border-white/10 bg-white/5 backdrop-blur-2xl p-8 shadow-2xl">

            <h2 className="text-2xl font-bold mb-5">
              Preview
            </h2>

            {output ? (

              <>
                <video
                  controls
                  className="w-full rounded-2xl border border-white/10"
                >
                  <source
                    src={output}
                    type="video/mp4"
                  />
                </video>

                <a
                  href={output}
                  download
                  className="mt-5 inline-block px-6 py-3 rounded-xl bg-green-600 hover:bg-green-500"
                >
                  Download Video
                </a>
              </>

            ) : (

              <div className="h-[350px] rounded-2xl border border-dashed border-white/10 flex items-center justify-center text-slate-500">

                Processed video will appear here

              </div>

            )}

          </div>

        </div>

      </div>

    </div>
  );
}

export default Dashboard;
