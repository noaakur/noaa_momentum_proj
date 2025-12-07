/**
 * API service for Team Presence Dashboard
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Get stored auth token
 */
export const getToken = () => localStorage.getItem('token');

/**
 * Store auth token
 */
export const setToken = (token) => localStorage.setItem('token', token);

/**
 * Remove auth token
 */
export const removeToken = () => localStorage.removeItem('token');

/**
 * Make authenticated API request
 */
async function authFetch(endpoint, options = {}) {
  const token = getToken();
  
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });
  
  if (response.status === 401) {
    removeToken();
    window.location.href = '/';
    throw new Error('Unauthorized');
  }
  
  return response;
}

/**
 * Login with username and password
 */
export async function login(username, password) {
  const response = await fetch(`${API_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Login failed');
  }
  
  const data = await response.json();
  setToken(data.access_token);
  return data;
}

/**
 * Logout - remove token
 */
export function logout() {
  removeToken();
}

/**
 * Get team members with optional status filter
 */
export async function getTeam(statusFilters = []) {
  let endpoint = '/team';
  
  if (statusFilters.length > 0) {
    const params = statusFilters.map(s => `status=${s}`).join('&');
    endpoint += `?${params}`;
  }
  
  const response = await authFetch(endpoint);
  
  if (!response.ok) {
    throw new Error('Failed to fetch team');
  }
  
  return response.json();
}

/**
 * Update current user's status
 */
export async function updateMyStatus(status) {
  const response = await authFetch('/me/status', {
    method: 'PATCH',
    body: JSON.stringify({ status }),
  });
  
  if (!response.ok) {
    throw new Error('Failed to update status');
  }
  
  return response.json();
}

/**
 * Status options
 */
export const STATUS_OPTIONS = [
  { value: 0, label: 'Working' },
  { value: 1, label: 'Working Remotely' },
  { value: 2, label: 'On Vacation' },
  { value: 3, label: 'Business Trip' },
];

