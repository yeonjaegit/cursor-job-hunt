import api from './client';
import { setLoginJustCompleted } from './client';

export { setLoginJustCompleted };

// baseURL이 /api/로 끝나므로 경로는 슬래시 없이 (axios 조합: baseURL + path)
export const authAPI = {
  login: (username, password) => api.post('auth/login', { username, password }),
  register: (username, email, password) => api.post('auth/register', { username, email, password }),
  refresh: (refreshToken) => api.post('auth/refresh', {}, { headers: { Authorization: `Bearer ${refreshToken}` } }),
  getMe: () => api.get('auth/me'),
};

export const dashboardAPI = {
  getStats: () => api.get('dashboard'),
  getPublicStats: () => api.get('public/dashboard'),
};

export const attendanceAPI = {
  getAll: () => api.get('attendance'),
  checkIn: () => api.post('attendance'),
  getStats: () => api.get('attendance/stats'),
  getPublicAll: () => api.get('public/attendance'),
};

export const scheduleAPI = {
  getAll: (dayOfWeek, weekStart) => api.get('schedules', {
    params: {
      ...(dayOfWeek != null && dayOfWeek !== '' ? { day_of_week: dayOfWeek } : {}),
      ...(weekStart ? { week_start: weekStart } : {}),
    },
  }),
  create: (data) => api.post('schedules', data),
  update: (id, data) => api.put(`schedules/${id}`, data),
  delete: (id) => api.delete(`schedules/${id}`),
  toggleActive: (id) => api.post(`schedules/${id}/toggle`),
  setDayOff: (dayOfWeek, weekStart) => api.post(`schedules/day-off/${dayOfWeek}`, { week_start: weekStart || null }),
  resetDay: (dayOfWeek, weekStart) => api.post(`schedules/reset-day/${dayOfWeek}`, { week_start: weekStart || null }),
  swap: (scheduleId, direction) => api.post('schedules/swap', { schedule_id: scheduleId, direction }),
  getChecks: (date) => api.get('schedule-checks', { params: date ? { date } : {} }),
  toggleCheck: (scheduleId, isChecked, date) => api.post('schedule-checks', { schedule_id: scheduleId, is_checked: isChecked, date }),
  getPublicAll: (dayOfWeek, weekStart) => api.get('public/schedules', {
    params: {
      ...(dayOfWeek != null && dayOfWeek !== '' ? { day_of_week: dayOfWeek } : {}),
      ...(weekStart ? { week_start: weekStart } : {}),
    },
  }),
};

export const companiesAPI = {
  getAll: (q) => api.get('companies', { params: q ? { q } : {} }),
  create: (data) => api.post('companies', data),
  update: (id, data) => api.put(`companies/${id}`, data),
  delete: (id) => api.delete(`companies/${id}`),
  getStats: () => api.get('companies/stats'),
  getPublicAll: (q) => api.get('public/companies', { params: q ? { q } : {} }),
};

export const codingAPI = {
  getAll: () => api.get('coding'),
  create: (data) => api.post('coding', data),
  update: (id, data) => api.put(`coding/${id}`, data),
  delete: (id) => api.delete(`coding/${id}`),
  getStats: () => api.get('coding/stats'),
  getPublicAll: () => api.get('public/coding'),
};

export default api;
