import { createContext, useContext, useState, useEffect } from 'react';
import { authAPI, setLoginJustCompleted } from '../api';
import { TOKEN_KEY, REFRESH_KEY } from '../api/client';

const defaultAuth = { isAdmin: false, user: null, login: async () => ({ success: false }), logout: () => {}, loading: true };
const AuthContext = createContext(defaultAuth);

export const AuthProvider = ({ children }) => {
  const [isAdmin, setIsAdmin] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = () => {
    const token = localStorage.getItem(TOKEN_KEY);
    const refreshToken = localStorage.getItem(REFRESH_KEY);
    const hasToken = (token && token.length >= 10) || (refreshToken && refreshToken.length >= 10);
    if (hasToken) setIsAdmin(true);
    setLoading(false);
  };

  const clearTokens = () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_KEY);
    setIsAdmin(false);
    setUser(null);
  };

  const login = async (username, password) => {
    try {
      const response = await authAPI.login(username, password);
      const token = response.data?.access_token || response.data?.token;
      const refresh = response.data?.refresh_token;
      if (!token || typeof token !== 'string') {
        return { success: false, message: '서버 응답 오류' };
      }
      localStorage.setItem(TOKEN_KEY, String(token).trim());
      if (refresh) localStorage.setItem(REFRESH_KEY, String(refresh).trim());
      setUser(response.data?.user || null);
      setIsAdmin(true);
      setLoginJustCompleted(); // 로그인 직후 토큰 삭제 방지
      return { success: true };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.error || '로그인에 실패했습니다.',
      };
    }
  };

  const logout = () => {
    clearTokens();
  };

  return (
    <AuthContext.Provider value={{ isAdmin, user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext) || defaultAuth;
