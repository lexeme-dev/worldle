import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import React, { useEffect } from "react";
import { Button, Card } from "react-bootstrap";
import { PlusCircle } from "react-bootstrap-icons";
import {
  createGameMutation,
  readCurrentGameOptions,
  readCurrentGameQueryKey,
  readGameOptions,
  readGameQueryKey,
} from "../client/@tanstack/react-query.gen";
import { useUser } from "../contexts/UserContext";
import "./GamePage.css";
import GamePlayer from "../components/GamePlayer";

const GamePage: React.FC = () => {
  const { uuid } = useUser();
  const queryClient = useQueryClient();

  const { data: currentGame, isSuccess: currentGameLoaded } = useQuery({
    ...readCurrentGameOptions({
      path: { user_client_uuid: uuid },
    }),
  });

  const { data: game } = useQuery({
    ...readGameOptions({
      path: { game_id: currentGame?.id },
    }),
    enabled: !!currentGame,
  });

  const createGame = useMutation({
    ...createGameMutation(),
    onSuccess: (newGame) => {
      queryClient.setQueryData(
        readCurrentGameQueryKey({
          path: { user_client_uuid: uuid },
        }),
        newGame,
      );
    },
  });

  const handleNewGame = () => {
    if (!uuid) return;
    createGame.mutate({
      body: { user_client_uuid: uuid },
    });
  };

  useEffect(() => {
    if (currentGameLoaded && !currentGame && !createGame.isPending && uuid) {
      handleNewGame();
    }
  }, [currentGameLoaded, currentGame, uuid]);

  return (
    <div className="game-page">
      <Card>
        <Card.Header className="d-flex justify-content-end align-items-center">
          <Button
            size="sm"
            onClick={handleNewGame}
            disabled={createGame.isPending}
          >
            <PlusCircle className="me-2" />
            {createGame.isPending ? "Creating..." : "New Game"}
          </Button>
        </Card.Header>
        <Card.Body>
          {game && <GamePlayer game={game} onNewGame={handleNewGame} />}
        </Card.Body>
      </Card>
    </div>
  );
};

export default GamePage;
