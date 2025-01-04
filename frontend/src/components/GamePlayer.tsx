import { useQuery } from "@tanstack/react-query";
import React, { useState } from "react";
import { CountryItem, GameRead } from "../client/types.gen";
import { useCountries } from "../contexts/CountriesContext";
import CountrySelect from "./CountrySelect";

interface GamePlayerProps {
  game: GameRead;
}

const GamePlayer: React.FC<GamePlayerProps> = ({ game }) => {
  const { countries } = useCountries();
  const [selectedCountry, setSelectedCountry] = useState<
    CountryItem | undefined
  >();

  const { data: svgContent } = useQuery({
    queryKey: ["countrySvg", game.answer_country.svg_url],
    queryFn: async () => {
      if (!game.answer_country.svg_url) return null;
      const response = await fetch(game.answer_country.svg_url);
      return response.text();
    },
    enabled: !!game.answer_country.svg_url,
    staleTime: 1000 * 60 * 60 * 24,
  });

  return (
    <div className="current-game">
      {svgContent && (
        <>
          <div
            className="country-svg"
            dangerouslySetInnerHTML={{ __html: svgContent }}
          />
          <div className="country-select-container">
            <CountrySelect
              countries={countries}
              selectedCountry={selectedCountry}
              onSelect={(country) => {
                setSelectedCountry(country);
                console.log("Selected:", country);
              }}
            />
          </div>
        </>
      )}
    </div>
  );
};

export default GamePlayer;
