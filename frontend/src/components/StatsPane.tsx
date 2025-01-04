import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import React from "react";
import { Card, Col, Row, Spinner } from "react-bootstrap";
import { readUserStatsOptions } from "../client/@tanstack/react-query.gen";
import { useUser } from "../contexts/UserContext";

const StatsPane: React.FC = () => {
  const { uuid } = useUser();

  const { data: stats, isLoading } = useQuery({
    ...readUserStatsOptions({
      path: { user_client_uuid: uuid },
    }),
    enabled: !!uuid,
  });

  if (isLoading) {
    return (
      <div className="content-container">
        <Spinner animation="border" variant="primary" />
        <div className="text-center">Loading...</div>
      </div>
    );
  }

  return (
    <motion.div
      className="content-container"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2 }}
    >
      <Card>
        <Card.Body>
          <Card.Title className="mb-3">Statistics</Card.Title>
          <Row className="text-center mb-4">
            {[
              { value: stats.num_played, label: "Played" },
              {
                value: `${Math.round(stats.win_rate * 100)}%`,
                label: "Win Rate",
              },
              { value: stats.current_streak, label: "Current Streak" },
              { value: stats.max_streak, label: "Max Streak" },
            ].map((stat, index) => (
              <Col key={stat.label}>
                <motion.h3
                  initial={{ opacity: 0, scale: 0.5 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.2, delay: index * 0.1 }}
                >
                  {stat.value}
                </motion.h3>
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.3, delay: index * 0.1 + 0.2 }}
                >
                  {stat.label}
                </motion.div>
              </Col>
            ))}
          </Row>

          <Card.Title className="mt-4 mb-3">Guess Distribution</Card.Title>
          {Object.entries(stats.guess_distribution)
            .sort(([a], [b]) => Number(a) - Number(b))
            .map(([guesses, count], index) => {
              const percentage = (count / stats.num_won) * 100;
              return (
                <motion.div
                  key={guesses}
                  className="mb-3"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.2, delay: index * 0.05 }}
                >
                  <div className="d-flex align-items-center">
                    <div style={{ width: "30px", fontWeight: "bold" }}>
                      {guesses}
                    </div>
                    <motion.div
                      className="bg-primary ms-2 px-3 py-2 rounded text-white"
                      initial={{ width: 0 }}
                      animate={{ width: `${Math.max(percentage, 8)}%` }}
                      transition={{ duration: 0.8, delay: index * 0.1 + 0.3 }}
                      style={{
                        minWidth: "50px",
                      }}
                    >
                      {count}
                    </motion.div>
                  </div>
                </motion.div>
              );
            })}
        </Card.Body>
      </Card>
    </motion.div>
  );
};

export default StatsPane;
