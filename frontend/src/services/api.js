import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api",
  timeout: 10000,
});

export const getHealth = () => api.get("/health").then((r) => r.data);

export default api;
