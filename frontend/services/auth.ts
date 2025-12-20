import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface JWTPayload {
  sub: string;  // email
  role: string; // user role
  id: number;   // user id
  exp: number;  // expiration timestamp
}

export const login = async (email: string, password: string) => {
  const params = new URLSearchParams();
  params.append('username', email);
  params.append('password', password);

  try {
    const response = await axios.post(`${API_BASE_URL}/api/v1/auth/login`, params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      const decoded = jwtDecode<JWTPayload>(response.data.access_token);
      localStorage.setItem('user', JSON.stringify({ email: decoded.sub, role: decoded.role }));
    }
    return response.data;
  } catch (error: any) {
    console.error("Login failed:", error);
    // Throw the error with the backend's message if available
    if (error.response && error.response.data && error.response.data.detail) {
      throw new Error(error.response.data.detail);
    }
    throw new Error("Login failed. Please try again.");
  }
};

export const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
};

export const getCurrentUser = () => {
  const userStr = localStorage.getItem('user');
  if (userStr) return JSON.parse(userStr);
  return null;
};

export const getToken = () => {
  return localStorage.getItem('token');
};
