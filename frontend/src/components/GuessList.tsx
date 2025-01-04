import { motion } from "framer-motion";
import React from "react";
import { ArrowRight, Check } from "react-bootstrap-icons";
import { GameStatus, GuessItem } from "../client/types.gen";

interface GuessListProps {
  guesses: GuessItem[];
  gameStatus: GameStatus;
}

const GuessList: React.FC<GuessListProps> = ({ guesses, gameStatus }) => {
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
                {Math.round(guess.distance_to_answer_miles)}mi
              </div>
              <div className="guess-direction">
                <ArrowRight
                  style={{
                    transform: `rotate(${guess.bearing_to_answer}deg)`,
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
