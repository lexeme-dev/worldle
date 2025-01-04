import { useQuery } from "@tanstack/react-query";
import React, { createContext, useContext } from "react";
import { CountryItem, DefaultService } from "../client";

interface CountriesContext {
  getCountry: (id: number) => CountryItem | undefined;
  countries: CountryItem[];
  isLoading: boolean;
}

const CountriesContext = createContext<CountriesContext | null>(null);

export const CountriesProvider: React.FC<{
  children: React.ReactNode;
}> = ({ children }) => {
  const { data: countries, isLoading } = useQuery({
    queryKey: ["countries"],
    queryFn: async () => {
      const { data } = await DefaultService.listCountries();
      return data;
    },
  });

  const getCountry = (id: number) =>
    countries?.find((country) => country.id === id);

  return (
    <CountriesContext.Provider
      value={{
        getCountry,
        countries: countries ?? [],
        isLoading,
      }}
    >
      {children}
    </CountriesContext.Provider>
  );
};

export const useCountries = () => {
  const context = useContext(CountriesContext);
  if (!context) {
    throw new Error("useCountries must be used within a CountriesProvider");
  }
  return context;
};
