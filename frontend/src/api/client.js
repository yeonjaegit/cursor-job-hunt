import axios from 'axios';

// 개발: 프록시 사용 (/api → 127.0.0.1:5000) = same-origin, 헤더 100% 전달
// 배포: VITE_API_URL 설정
const API_BASE = import.meta.env.VITE_API_URL ?? '';
const baseURL = API_BASE ? `${String(API_BASE).replace(/\/$/, '')}/api/` : '/api/';

export const TOKEN_KEY = 'token';
export const REFRESH_KEY = 'refresh_token';

let loginJustCompletedAt = 0;
export const setLoginJustCompleted = () => { loginJustCompletedAt = Date.now(); };

const api = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: false,
});

let isRefreshing = false;
let refreshSubscribers = [];

const onRefreshed = (token) => {
  refreshSubscribers.forEach((cb) => cb(token));
  refreshSubscribers = [];
};

const addRefreshSubscriber = (cb) => refreshSubscribers.push(cb);

const onRefreshFailed = () => {
  refreshSubscribers.forEach((cb) => cb(null));
  refreshSubscribers = [];
  // 토큰 자동 삭제 안 함 - 사용자가 직접 로그아웃할 때만 삭제
};

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(TOKEN_KEY);
    if (token) config.headers.Authorization = `Bearer ${String(token).trim()}`;
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status !== 401 && error.response?.status !== 422) return Promise.reject(error);
    if (originalRequest.url?.includes('auth/login') || originalRequest.url?.includes('auth/refresh')) return Promise.reject(error);
    const refreshToken = localStorage.getItem(REFRESH_KEY);
    if (!refreshToken) return Promise.reject(error);
    if (!originalRequest._retry) {
      originalRequest._retry = true;
      if (!isRefreshing) {
        isRefreshing = true;
        try {
          const res = await axios.post(`${baseURL.replace(/\/$/, '')}/auth/refresh`, {}, { headers: { Authorization: `Bearer ${String(refreshToken).trim()}` } });
          const newToken = res.data?.access_token;
          const newRefresh = res.data?.refresh_token;
          if (newToken) {
            localStorage.setItem(TOKEN_KEY, newToken);
            if (newRefresh) localStorage.setItem(REFRESH_KEY, newRefresh);
            isRefreshing = false;
            onRefreshed(newToken);
            originalRequest.headers.Authorization = `Bearer ${newToken}`;
            return api(originalRequest);
          }
        } catch { onRefreshFailed(); }
        isRefreshing = false;
      } else {
        return new Promise((resolve, reject) => {
          addRefreshSubscriber((token) => {
            if (!token) return reject(error);
            originalRequest.headers.Authorization = `Bearer ${token}`;
            resolve(api(originalRequest));
          });
        });
      }
    }
    return Promise.reject(error);
  }
);

export default api;
export { baseURL };
