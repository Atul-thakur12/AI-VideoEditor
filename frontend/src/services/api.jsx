import axios from "axios";

export const processVideo = async (video, prompt) => {
  const formData = new FormData();
  formData.append("video", video);
  formData.append("prompt", prompt);

  return axios.post("http://localhost:8000/process-video", formData);
};