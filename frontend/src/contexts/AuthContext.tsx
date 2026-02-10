import React, { createContext, useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../lib/api";

type User = { id: string; email: string } | null;

type AuthContextType = {
  user: User;
  loading: boolean;
  signup: (email: string, password: string, name?: string) => Promise<void>;
  signin: (email: string, password: string) => Promise<void>;
  oauthLogin: (access: string, refresh: string) => Promise<void>;
  signout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const init = async () => {
      const token = localStorage.getItem("access_token");
      if (!token) return;
      try {
        const resp = await api.get("/api/auth/me");
        const u = resp.data;
        setUser({ id: u.id, email: u.email });
      } catch (e) {
        // token invalid or expired
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
      }
    };

    init();
  }, []);

  const signup = async (email: string, password: string, name?: string) => {
    setLoading(true);
    try {
      const resp = await api.post("/api/auth/register", { email, password, full_name: name });
      // server returns verify_token but not access tokens until verification — we'll just set user email
      setUser({ id: resp.data.user_id, email });
      navigate("/");
    } finally {
      setLoading(false);
    }
  };

  const signin = async (email: string, password: string) => {
    setLoading(true);
    try {
      const resp = await api.post("/api/auth/login", { email, password });
      const { access_token, refresh_token } = resp.data;
      await oauthLogin(access_token, refresh_token);
    } finally {
      setLoading(false);
    }
  };

  const oauthLogin = async (access: string, refresh: string) => {
    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);
    try {
      const resp = await api.get("/api/auth/me");
      const u = resp.data;
      setUser({ id: u.id, email: u.email });
    } catch (e) {
      setUser({ id: "", email: "" });
    }
    navigate("/");
  };

  const signout = () => {
    const refresh = localStorage.getItem("refresh_token");
    if (refresh) {
      api.post("/api/auth/logout", { refresh_token: refresh }).catch(() => {});
    }
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setUser(null);
    navigate("/");
  };

  return (
    <AuthContext.Provider value={{ user, loading, signup, signin, oauthLogin, signout }}>{children}</AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};
