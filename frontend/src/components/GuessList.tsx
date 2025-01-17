import { motion } from "framer-motion";
import React from "react";
import { ArrowRight, Check } from "react-bootstrap-icons";
import { GameStatus, GuessItem } from "../client/types.gen";
import { DistanceUnit, useSettings } from "../contexts/SettingsContext";

interface GuessListProps {
  guesses: GuessItem[];
  gameStatus: GameStatus;
}

const GuessList: React.FC<GuessListProps> = ({ guesses, gameStatus }) => {
  const { distanceUnit } = useSettings();

  return (
    <div className="guess-list">
      {guesses.map((guess, index) => (
        <motion.div
          key={guess.id}
          className={`guess-item ${guess.is_correct ? "correct" : ""}`}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: index * 0.1 }}
        >
          <div className="guess-country">{guess.guessed_country.name}</div>
          {guess.is_correct ? (
            <div className="guess-correct">
              <Check className="check-icon" />
            </div>
          ) : (
            <>
              <div className="guess-distance">
                {distanceUnit === DistanceUnit.MILES
                  ? `${Math.round(guess.distance_to_answer_miles)}mi`
                  : `${Math.round(guess.distance_to_answer_km)}km`}
              </div>
              <div className="guess-direction">
                <ArrowRight
                  style={{
                    transform: `rotate(${
                      {
                        NORTH: 270,
                        NORTH_EAST: 315,
                        EAST: 0,
                        SOUTH_EAST: 45,
                        SOUTH: 90,
                        SOUTH_WEST: 135,
                        WEST: 180,
                        NORTH_WEST: 225,
                      }[guess.compass_direction_to_answer]
                    }deg)`,
                  }}
                />
              </div>
              <div className="guess-proximity">
                {(guess.proximity_prop * 100).toFixed()}%
              </div>
            </>
          )}
        </motion.div>
      ))}
      {gameStatus === GameStatus.IN_PROGRESS &&
        [...Array(6 - guesses.length)].map((_, i) => (
          <div key={`empty-${i}`} className="guess-item empty" />
        ))}
      <div className="guess-counter">GUESS {guesses.length} / 6</div>
    </div>
  );
};

export default GuessList;
