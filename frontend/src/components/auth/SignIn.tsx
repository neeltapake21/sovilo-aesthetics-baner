import React, { useEffect, useRef } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { useAuth } from "../../contexts/AuthContext";
import api from "../../lib/api";
import { useNavigate } from "react-router-dom";

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(1),
});

type FormData = z.infer<typeof schema>;

export const SignIn: React.FC = () => {
  const { signin, loading, oauthLogin } = useAuth();
  const { register, handleSubmit } = useForm<FormData>({ resolver: zodResolver(schema) });
  const googleButtonRef = useRef<HTMLDivElement | null>(null);
  const navigate = useNavigate();

  const onSubmit = async (data: FormData) => {
    await signin(data.email, data.password);
  };

  useEffect(() => {
    const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;
    if (!clientId) return;
    // initialize Google Identity Services
    const handleCredentialResponse = async (response: any) => {
      const idToken = response?.credential;
      if (!idToken) return;
      try {
        const resp = await api.post("/api/auth/google", { id_token: idToken });
        const { access_token, refresh_token } = resp.data;
        await oauthLogin(access_token, refresh_token);
      } catch (e) {
        console.error("Google sign-in failed", e);
      }
    };

    // initialize when available
    const tryInit = () => {
      // @ts-ignore
      const g = (window as any).google;
      if (g && g.accounts && googleButtonRef.current) {
        g.accounts.id.initialize({ client_id: clientId, callback: handleCredentialResponse });
        g.accounts.id.renderButton(googleButtonRef.current, { theme: "outline", size: "large" });
        return true;
      }
      return false;
    };

    if (!tryInit()) {
      const id = window.setInterval(() => {
        if (tryInit()) {
          window.clearInterval(id);
        }
      }, 250);
    }
  }, [navigate]);

  return (
    <div className="max-w-md mx-auto p-6">
      <h2 className="text-2xl font-semibold mb-4">Sign in</h2>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label className="block text-sm font-medium">Email</label>
          <input {...register("email")} className="mt-1 w-full rounded border px-3 py-2" />
        </div>
        <div>
          <label className="block text-sm font-medium">Password</label>
          <input type="password" {...register("password")} className="mt-1 w-full rounded border px-3 py-2" />
        </div>
        <div>
          <button type="submit" disabled={loading} className="w-full rounded bg-primary px-4 py-2 text-white">
            {loading ? "Signing in..." : "Sign in"}
          </button>
        </div>
        <div className="mt-4">
          <div ref={googleButtonRef} />
        </div>
      </form>
    </div>
  );
};
