import { createContext, useContext, useState } from "react";

export enum DistanceUnit {
  MILES = "miles",
  KILOMETERS = "kilometers",
}

interface SettingsContextType {
  distanceUnit: DistanceUnit;
  setDistanceUnit: (unit: DistanceUnit) => void;
}

const SettingsContext = createContext<SettingsContextType | undefined>(
  undefined,
);

export const SettingsProvider = ({
  children,
}: { children: React.ReactNode }) => {
  const [distanceUnit, setDistanceUnit] = useState(DistanceUnit.MILES);

  return (
    <SettingsContext.Provider
      value={{
        distanceUnit,
        setDistanceUnit,
      }}
    >
      {children}
    </SettingsContext.Provider>
  );
};

export const useSettings = () => {
  const context = useContext(SettingsContext);
  if (!context) {
    throw new Error("useSettings must be used within a SettingsProvider");
  }
  return context;
};
