import React from "react";
import { Col, Container, Row } from "react-bootstrap";
import { Link, Route, Routes } from "react-router-dom";
import ReadyGate from "./components/ReadyGate";
import GamePage from "./pages/GamePage";

import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

const App: React.FC = () => {
  return (
    <Container fluid className="app-container">
      <Row className="header">
        <Col className="text-center py-3">
          <h1 className="app-title">
            <Link to="/" className="text-decoration-none">
              Worldle
            </Link>
          </h1>
        </Col>
      </Row>
      <Container className="main-content py-2">
        <Row>
          <Col>
            <Routes>
              <Route element={<ReadyGate />}>
                <Route path="/" element={<GamePage />} />
              </Route>
            </Routes>
          </Col>
        </Row>
      </Container>
    </Container>
  );
};

export default App;
