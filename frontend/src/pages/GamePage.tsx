import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import React from "react";
import { Button, Card } from "react-bootstrap";
import { PlusCircle } from "react-bootstrap-icons";
import {
  createGameMutation,
  readCurrentGameOptions,
  readCurrentGameQueryKey,
} from "../client/@tanstack/react-query.gen";
import { useUser } from "../contexts/UserContext";
import "./GamePage.css";
import GamePlayer from "../components/GamePlayer";

const GamePage: React.FC = () => {
  const { uuid } = useUser();
  const queryClient = useQueryClient();

  const { data: currentGame } = useQuery({
    ...readCurrentGameOptions({
      path: { user_client_uuid: uuid },
    }),
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
          {currentGame && <GamePlayer game={currentGame} />}
        </Card.Body>
      </Card>
    </div>
  );
};

export default GamePage;
