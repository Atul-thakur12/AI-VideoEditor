import { useRef, useState } from "react";
import { FaCloudUploadAlt, FaVideo } from "react-icons/fa";
import { motion } from "framer-motion";

function UploadBox({ setVideo, video }) {
  const fileInputRef = useRef(null);
  const [dragActive, setDragActive] = useState(false);

  const handleFile = (file) => {
    if (!file) return;
    setVideo(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);

    const file = e.dataTransfer.files[0];
    handleFile(file);
  };

  const formatSize = (bytes) => {
    if (!bytes) return "";
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  return (
    <div className="mb-8">
      <motion.div
        whileHover={{ scale: 1.01 }}
        onClick={() => fileInputRef.current.click()}
        onDragOver={(e) => {
          e.preventDefault();
          setDragActive(true);
        }}
        onDragLeave={() => setDragActive(false)}
        onDrop={handleDrop}
        className={`relative rounded-3xl p-10 cursor-pointer border-2 border-dashed transition-all duration-300 ${
          dragActive
            ? "border-purple-400 bg-purple-500/20 shadow-[0_0_40px_rgba(168,85,247,0.4)]"
            : "border-white/20 bg-white/5 hover:bg-white/10"
        }`}
      >
        {!video ? (
          <div className="text-center">
            <motion.div
              animate={{ y: [0, -10, 0] }}
              transition={{ repeat: Infinity, duration: 2 }}
            >
              <FaCloudUploadAlt className="text-6xl mx-auto mb-4 text-purple-400" />
            </motion.div>

            <h3 className="text-2xl font-semibold mb-2">
              Drop your video here
            </h3>

            <p className="text-gray-300 mb-4">
              Drag & drop or click to browse
            </p>

            <button
              type="button"
              className="px-6 py-3 rounded-xl bg-gradient-r from-purple-600 to-pink-500 font-medium"
            >
              Choose Video
            </button>
          </div>
        ) : (
          <div className="space-y-5">
            <div className="flex items-center gap-4 bg-white/10 rounded-2xl p-4">
              <FaVideo className="text-3xl text-purple-400" />

              <div className="flex-1">
                <p className="font-semibold text-lg truncate">{video.name}</p>
                <p className="text-gray-300 text-sm">
                  {formatSize(video.size)}
                </p>
              </div>

              <button
                type="button"
                className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-700"
              >
                Change
              </button>
            </div>

            <video
              controls
              className="w-full rounded-2xl max-h-96 object-cover"
              src={URL.createObjectURL(video)}
            />
          </div>
        )}

        <input
          ref={fileInputRef}
          type="file"
          accept="video/*"
          hidden
          onChange={(e) => handleFile(e.target.files[0])}
        />
      </motion.div>
    </div>
  );
}

export default UploadBox;