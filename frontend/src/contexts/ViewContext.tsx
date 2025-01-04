import { createContext, useContext, useState } from "react";

export enum ActivePane {
  MAIN = "main",
  SETTINGS = "settings",
  STATS = "stats",
}

interface ViewContextType {
  activePane: ActivePane;
  setActivePane: (pane: ActivePane) => void;
}

const ViewContext = createContext<ViewContextType | undefined>(undefined);

export const ViewProvider = ({ children }: { children: React.ReactNode }) => {
  const [activePane, setActivePane] = useState(ActivePane.MAIN);

  return (
    <ViewContext.Provider
      value={{
        activePane,
        setActivePane,
      }}
    >
      {children}
    </ViewContext.Provider>
  );
};

export const useView = () => {
  const context = useContext(ViewContext);
  if (!context) {
    throw new Error("useView must be used within a ViewProvider");
  }
  return context;
};
