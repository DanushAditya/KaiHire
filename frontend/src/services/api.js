import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 second timeout
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Add response interceptor for better error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ECONNABORTED') {
      console.error('Request timeout - is the backend server running?');
    } else if (error.message === 'Network Error') {
      console.error('Network Error - Backend server is not running on http://localhost:8000');
      console.error('Please start the backend server with: uvicorn app.main:app --reload');
    }
    return Promise.reject(error);
  }
);

// Auth
export const register = (data) => api.post('/auth/register', data);
export const login = (data) => api.post('/auth/login', data);
export const getCurrentUser = () => api.get('/auth/me');

// Student
export const getStudentProfile = () => api.get('/student/profile');
export const updateStudentProfile = (data) => api.put('/student/profile', data);
export const uploadResume = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/student/resume/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};
export const createAssessment = (data) => api.post('/student/assessment', data);
export const getAssessments = () => api.get('/student/assessments');
export const generatePlan = (planType) => api.post(`/student/plan/generate?plan_type=${planType}`);
export const getPlans = () => api.get('/student/plans');
export const getPlanTasks = (planId) => api.get(`/student/plan/${planId}/tasks`);
export const completeTask = (taskId) => api.post(`/student/task/${taskId}/complete`);

// Challenges
export const getChallenges = () => api.get('/challenges/');
export const enrollChallenge = (data) => api.post('/challenges/enroll', data);
export const getMyChallenges = () => api.get('/challenges/my-challenges');
export const updateChallengeProgress = (data) => api.put('/challenges/progress', data);

// Friends
export const sendFriendRequest = (data) => api.post('/friends/request', data);
export const getFriendRequests = () => api.get('/friends/requests');
export const acceptFriendRequest = (friendshipId) => api.post(`/friends/accept/${friendshipId}`);
export const getFriends = () => api.get('/friends/list');

// Leaderboard
export const getClassLeaderboard = (params) => api.get('/leaderboard/class', { params });
export const getBranchLeaderboard = (params) => api.get('/leaderboard/branch', { params });
export const getCollegeLeaderboard = (params) => api.get('/leaderboard/college', { params });

// HR
export const getHRProfile = () => api.get('/hr/profile');
export const filterStudents = (params) => api.get('/hr/students', { params });
export const getStudentDetail = (studentId) => api.get(`/hr/student/${studentId}`);
export const getAnalytics = () => api.get('/hr/analytics');
export const exportStudents = (params) => api.get('/hr/export', { params, responseType: 'blob' });

export default api;
