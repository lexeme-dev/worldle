import React from "react";
import { Col, Container, Row } from "react-bootstrap";
import { Route, Routes } from "react-router-dom";
import Footer from "./components/Footer";
import Header from "./components/Header";
import ReadyGate from "./components/ReadyGate";
import ViewGate from "./components/ViewGate";
import { SettingsProvider } from "./contexts/SettingsContext";
import GamePage from "./pages/GamePage";

import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

const App: React.FC = () => {
  return (
    <SettingsProvider>
      <Container fluid className="app-container">
        <Header />
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
        <Footer />
      </Container>
    </SettingsProvider>
  );
};

export default App;
