import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import React, { useState } from "react";
import { Button } from "react-bootstrap";
import { Trophy } from "react-bootstrap-icons";
import { DefaultService } from "../client";
import { readGameQueryKey } from "../client/@tanstack/react-query.gen";
import {
  CountryItem,
  GameRead,
  GameStatus,
  GuessRead,
} from "../client/types.gen";
import { useCountries } from "../contexts/CountriesContext";
import CountrySelect from "./CountrySelect";
import GuessList from "./GuessList";

interface GamePlayerProps {
  game: GameRead;
  onNewGame: () => void;
}

const GamePlayer: React.FC<GamePlayerProps> = ({ game, onNewGame }) => {
  const { countries } = useCountries();
  const [selectedCountry, setSelectedCountry] = useState<
    CountryItem | undefined
  >();
  const queryClient = useQueryClient();

  const isGameOver = game.status !== GameStatus.IN_PROGRESS;

  const guessMutation = useMutation({
    mutationFn: async () => {
      if (!selectedCountry) return;
      const { data } = await DefaultService.createGuess({
        path: { game_id: game.id },
        body: { guessed_country_id: selectedCountry.id },
      });
      return data;
    },
    onSuccess: (guess: GuessRead) => {
      queryClient.setQueryData(
        readGameQueryKey({ path: { game_id: game.id } }),
        guess.game,
      );
      setSelectedCountry(undefined);
    },
  });

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
          {isGameOver ? (
            <div className="game-over-container">
              {game.status === GameStatus.WON && (
                <div className="victory-message">
                  <Trophy className="victory-icon" />
                  <div className="victory-text">
                    Congratulations! You won in {game.guesses.length}{" "}
                    {game.guesses.length === 1 ? "guess" : "guesses"}!
                  </div>
                </div>
              )}
              {game.status === GameStatus.LOST && (
                <div className="defeat-message">
                  The country was {game.answer_country.name}.
                </div>
              )}
              <Button
                variant="primary"
                className="mt-3 new-game-button"
                onClick={onNewGame}
              >
                Play Again
              </Button>
            </div>
          ) : (
            <div className="country-select-container">
              <CountrySelect
                countries={countries}
                selectedCountry={selectedCountry}
                onSelect={setSelectedCountry}
              />
              <Button
                className="mt-3 w-100"
                disabled={!selectedCountry || guessMutation.isPending}
                onClick={() => guessMutation.mutate()}
              >
                Make Guess
              </Button>
            </div>
          )}
          <GuessList guesses={game.guesses} gameStatus={game.status} />
        </>
      )}
    </div>
  );
};

export default GamePlayer;
