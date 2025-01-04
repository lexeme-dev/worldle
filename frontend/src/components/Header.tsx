import React from "react";
import { Col, Container, Row } from "react-bootstrap";
import { BarChartFill, Gear } from "react-bootstrap-icons";
import { Link } from "react-router-dom";
import { useUser } from "../contexts/UserContext";
import { ActivePane, useView } from "../contexts/ViewContext";
import "./Header.css";

const Header: React.FC = () => {
  const { activePane, setActivePane } = useView();
  const { isLoading } = useUser();

  const togglePane = (pane: ActivePane) => {
    if (isLoading) return;
    setActivePane(activePane === pane ? ActivePane.MAIN : pane);
  };

  return (
    <Row className="header">
      <Col>
        <Container className="position-relative">
          <h1 className="app-title text-center py-3">
            <Link
              to="/"
              onClick={() => setActivePane(ActivePane.MAIN)}
              className="text-decoration-none"
            >
              Worldle
            </Link>
          </h1>
          <div className="header-icons">
            <BarChartFill
              className={`header-icon ${activePane === ActivePane.STATS ? "active" : ""} ${
                isLoading ? "disabled" : ""
              }`}
              onClick={() => togglePane(ActivePane.STATS)}
            />
            <Gear
              className={`header-icon ${activePane === ActivePane.SETTINGS ? "active" : ""} ${
                isLoading ? "disabled" : ""
              }`}
              onClick={() => togglePane(ActivePane.SETTINGS)}
            />
          </div>
        </Container>
      </Col>
    </Row>
  );
};

export default Header;
