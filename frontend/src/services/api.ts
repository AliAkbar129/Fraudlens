import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:3000/api',
  timeout: 10000,
});

api.interceptors.request.use(config => {
  const token = localStorage.getItem('fraudlens_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Mock response for demo purposes
api.interceptors.response.use(
  response => response,
  error => {
    console.warn('API Error (returning mock data):', error);
    return Promise.resolve({ data: [] }); 
  }
);

export const dashboardService = {
  getStats: () => api.get('/dashboard/stats'),
  getTrends: () => api.get('/dashboard/trends'),
};

export const transactionService = {
  list: (params?: any) => api.get('/transactions', { params }),
  get: (id: string) => api.get(`/transactions/${id}`),
};

export const caseService = {
  list: (params?: any) => api.get('/cases', { params }),
  get: (id: string) => api.get(`/cases/${id}`),
  update: (id: string, data: any) => api.patch(`/cases/${id}`, data),
};

export default api;
