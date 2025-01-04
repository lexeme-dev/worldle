import React from "react";
import { Col, Container, Row } from "react-bootstrap";
import { BarChartFill, Gear } from "react-bootstrap-icons";
import { Link } from "react-router-dom";
import { ActivePane, useView } from "../contexts/ViewContext";
import "./Header.css";

const Header: React.FC = () => {
  const { activePane, setActivePane } = useView();

  const togglePane = (pane: ActivePane) => {
    setActivePane(activePane === pane ? ActivePane.MAIN : pane);
  };

  return (
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
  );
};

export default Header;
