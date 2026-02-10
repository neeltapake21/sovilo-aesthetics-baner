import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

export default defineConfig({
  plugins: [react()],
  // Prevent Vite from pre-bundling @swc/core which can cause
  // duplicate runtime helpers (e.g. __vite__injectQuery) in dev.
  optimizeDeps: {
    exclude: ["@swc/core"],
  },
  ssr: {
    noExternal: ["@swc/core"],
  },
  server: {
    port: 5173,
  },
});

