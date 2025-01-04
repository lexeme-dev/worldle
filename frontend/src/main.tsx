import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import "./index.css";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter } from "react-router-dom";
import { client } from "./client";
import { CountriesProvider } from "./contexts/CountriesContext.tsx";
import { UserProvider } from "./contexts/UserContext.tsx";
import { ViewProvider } from "./contexts/ViewContext.tsx";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 10000,
    },
  },
});
client.setConfig({
  baseUrl: import.meta.env.VITE_WORLDLE_API_URL || "http://poirot:8101",
});

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <UserProvider>
        <CountriesProvider>
          <ViewProvider>
            <BrowserRouter>
              <App />
            </BrowserRouter>
          </ViewProvider>
        </CountriesProvider>
      </UserProvider>
    </QueryClientProvider>
  </StrictMode>,
);
