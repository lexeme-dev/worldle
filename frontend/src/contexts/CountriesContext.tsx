import { useQuery } from "@tanstack/react-query";
import React, { createContext, useContext } from "react";
import { CountryItem } from "../client";
import { listCountriesOptions } from "../client/@tanstack/react-query.gen";

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
    ...listCountriesOptions(),
    staleTime: 1000 * 60 * 60 * 24,
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
