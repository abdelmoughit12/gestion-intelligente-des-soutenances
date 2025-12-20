import { useEffect, useState } from 'react';
import { getCurrentUser, logout, getToken } from '@/services/auth';
import { jwtDecode } from 'jwt-decode';
import { User } from '@/types/soutenance';

interface JWTPayload {
  sub: string;
  role: string;
  id: number;
  exp: number;
}

export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getToken();
    if (token) {
      try {
        const decodedToken = jwtDecode<JWTPayload>(token);
        if (decodedToken.exp * 1000 < Date.now()) {
          logout();
          setUser(null);
        } else {
          setUser(getCurrentUser());
        }
      } catch (error) {
        console.error("Invalid token:", error);
        logout();
        setUser(null);
      }
    }
    setLoading(false);
  }, []);

  return { user, loading };
};
