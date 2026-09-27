import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    "Content-Type": "application/json"
  },
  timeout: 60000 // 60s — LLM responses can be slow
});

/**
 * Convert any axios/network error into a friendly, user-facing message.
 * Prefers the backend's `detail` field (our endpoints always send one).
 */
export function getFriendlyErrorMessage(error) {
  if (error?.code === "ECONNABORTED") {
    return "The mentor took too long to reply. Please try again.";
  }

  if (!error?.response) {
    // Network error / backend down / CORS / invalid VITE_API_URL
    return "Cannot reach the mentor service. Check your connection and the API URL.";
  }

  const { status, data } = error.response;
  const detail = typeof data?.detail === "string" ? data.detail : null;

  if (detail) return detail;

  switch (status) {
    case 400:
      return "Invalid request. Please rephrase your message.";
    case 422:
      return "Your message could not be processed. Please rephrase and try again.";
    case 429:
      return "The mentor is receiving too many requests. Please wait a moment and try again.";
    case 500:
      return "Something went wrong on our side. Please try again.";
    case 502:
    case 503:
      return "The mentor service is temporarily unavailable. Please try again shortly.";
    case 504:
      return "The mentor service timed out. Please try again.";
    default:
      return "Something went wrong. Please try again.";
  }
}

export default api;
