const API_URL = "http://localhost:8080/api";
function getToken() {
  if (typeof window !== "undefined") {
    return localStorage.getItem("access_token");
  }
  return null;
}
function setToken(token) {
  if (typeof window !== "undefined") {
    localStorage.setItem("access_token", token);
  }
}
function clearToken() {
  if (typeof window !== "undefined") {
    localStorage.removeItem("access_token");
  }
}
async function apiRequest(endpoint, options = {}) {
  const token = getToken();
  const headers = {
    "Content-Type": "application/json",
    ...options.headers
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
    credentials: "include"
    // For cookies
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "An error occurred" }));
    throw new Error(error.detail || `HTTP error! status: ${response.status}`);
  }
  return response.json();
}
const authApi = {
  async register(email, password) {
    return apiRequest("/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password })
    });
  },
  async login(email, password) {
    const data = await apiRequest("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password })
    });
    if (data.accessToken) {
      setToken(data.accessToken);
    }
    return data;
  },
  async logout() {
    clearToken();
    return { success: true };
  },
  async getCurrentUser() {
    const token = getToken();
    if (!token) throw new Error("No token found");
    const payload = JSON.parse(atob(token.split(".")[1]));
    return { id: parseInt(payload.sub), role: payload.role };
  },
  async refresh(refreshToken) {
    const data = await apiRequest("/auth/refresh", {
      method: "POST",
      headers: { "Authorization": `Bearer ${refreshToken}` }
    });
    if (data.accessToken) {
      setToken(data.accessToken);
    }
    return data;
  }
};
const leaderboardApi = {
  async getLeaderboard(sortBy = "solved", problemId, limit = 100) {
    const params = new URLSearchParams();
    params.append("sortBy", sortBy);
    if (problemId) params.append("problemId", problemId.toString());
    params.append("limit", limit.toString());
    return apiRequest(`/leaderboard?${params.toString()}`);
  }
};
export {
  authApi as a,
  clearToken as c,
  leaderboardApi as l
};
