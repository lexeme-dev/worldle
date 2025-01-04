import React from "react";
import Select from "react-select";
import { CountryItem } from "../client/types.gen";

interface CountrySelectProps {
  countries: CountryItem[];
  selectedCountry: CountryItem | undefined;
  onSelect: (country: CountryItem | undefined) => void;
}

const CountrySelect: React.FC<CountrySelectProps> = ({
  onSelect,
  countries,
  selectedCountry,
}) => {
  return (
    <Select
      options={countries}
      value={selectedCountry}
      onChange={(option) => onSelect(option as CountryItem)}
      getOptionLabel={(option) => option.name}
      getOptionValue={(option) => option.id.toString()}
      placeholder="Select a country..."
      className="country-select"
      classNamePrefix="country-select"
      isClearable={true}
    />
  );
};

export default CountrySelect;
