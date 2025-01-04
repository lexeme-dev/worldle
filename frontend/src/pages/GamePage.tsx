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

  const { data: svgContent } = useQuery({
    queryKey: ["countrySvg", currentGame?.answer_country.svg_url],
    queryFn: async () => {
      if (!currentGame?.answer_country.svg_url) return null;
      const response = await fetch(currentGame.answer_country.svg_url);
      return response.text();
    },
    enabled: !!currentGame?.answer_country.svg_url,
  });

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
          {svgContent && (
            <div className="current-game">
              <div
                dangerouslySetInnerHTML={{ __html: svgContent }}
                className="country-svg"
              />
            </div>
          )}
        </Card.Body>
      </Card>
    </div>
  );
};

export default GamePage;
