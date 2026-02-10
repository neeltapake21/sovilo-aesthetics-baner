import React, { useEffect, useRef } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { useAuth } from "../../contexts/AuthContext";
import api from "../../lib/api";

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  full_name: z.string().optional(),
});

type FormData = z.infer<typeof schema>;

export const SignUp: React.FC = () => {
  const { signup, loading, oauthLogin } = useAuth();
  const { register, handleSubmit, formState } = useForm<FormData>({ resolver: zodResolver(schema) });
  const googleButtonRef = useRef<HTMLDivElement | null>(null);

  const onSubmit = async (data: FormData) => {
    await signup(data.email, data.password, data.full_name);
  };

  useEffect(() => {
    const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;
    if (!clientId) return;

    const handleCredentialResponse = async (response: any) => {
      const idToken = response?.credential;
      if (!idToken) return;
      try {
        const resp = await api.post("/api/auth/google", { id_token: idToken });
        const { access_token, refresh_token } = resp.data;
        await oauthLogin(access_token, refresh_token);
      } catch (e) {
        console.error("Google sign-up failed", e);
      }
    };

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
        if (tryInit()) window.clearInterval(id);
      }, 250);
    }
  }, [oauthLogin]);

  return (
    <div className="max-w-md mx-auto p-6">
      <h2 className="text-2xl font-semibold mb-4">Create account</h2>
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
          <label className="block text-sm font-medium">Full name (optional)</label>
          <input {...register("full_name")} className="mt-1 w-full rounded border px-3 py-2" />
        </div>
        <div>
          <button type="submit" disabled={loading} className="w-full rounded bg-primary px-4 py-2 text-white">
            {loading ? "Creating..." : "Create account"}
          </button>
        </div>
        <div className="mt-4">
          <div ref={googleButtonRef} />
        </div>
      </form>
    </div>
  );
};
