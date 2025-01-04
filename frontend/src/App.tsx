import React from "react";
import { Col, Container, Row, Stack } from "react-bootstrap";
import { BarChartFill, Gear, Github } from "react-bootstrap-icons";
import { Link, Route, Routes } from "react-router-dom";
import ReadyGate from "./components/ReadyGate";
import ViewGate from "./components/ViewGate";
import { ActivePane, useView } from "./contexts/ViewContext";
import GamePage from "./pages/GamePage";

import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

const App: React.FC = () => {
  const { activePane, setActivePane } = useView();

  const togglePane = (pane: ActivePane) => {
    setActivePane(activePane === pane ? ActivePane.MAIN : pane);
  };

  return (
    <Container fluid className="app-container">
      <Row className="header">
        <Col>
          <Container className="position-relative">
            <h1 className="app-title text-center py-3">
              <Link to="/" className="text-decoration-none">
                Worldle
              </Link>
            </h1>
            <div className="header-icons">
              <BarChartFill
                className={`header-icon ${activePane === ActivePane.STATS ? "active" : ""}`}
                onClick={() => togglePane(ActivePane.STATS)}
              />
              <Gear
                className={`header-icon ${activePane === ActivePane.SETTINGS ? "active" : ""}`}
                onClick={() => togglePane(ActivePane.SETTINGS)}
              />
            </div>
          </Container>
        </Col>
      </Row>
      <Container className="main-content py-2">
        <Row>
          <Col>
            <Routes>
              <Route element={<ReadyGate />}>
                <Route element={<ViewGate />}>
                  <Route path="/" element={<GamePage />} />
                </Route>
              </Route>
            </Routes>
          </Col>
        </Row>
      </Container>
      <footer className="app-footer">
        <Stack
          direction="horizontal"
          gap={2}
          className="justify-content-center align-items-center"
        >
          <span>Built by Faiz Surani</span>
          <a
            href="https://github.com/lexeme-dev/worldle"
            target="_blank"
            rel="noopener noreferrer"
          >
            <Github size={18} />
          </a>
        </Stack>
      </footer>
    </Container>
  );
};

export default App;
