import React from "react";
import { Card, Form } from "react-bootstrap";
import { DistanceUnit, useSettings } from "../contexts/SettingsContext";

const SettingsPane: React.FC = () => {
  const { distanceUnit, setDistanceUnit } = useSettings();

  return (
    <div className="content-container">
      <Card>
        <Card.Body>
          <Card.Title className="mb-4">Settings</Card.Title>
          <Form>
            <Form.Group className="mb-3">
              <Form.Label>Distance Unit</Form.Label>
              <Form.Select
                value={distanceUnit}
                onChange={(e) =>
                  setDistanceUnit(e.target.value as DistanceUnit)
                }
              >
                <option value={DistanceUnit.MILES}>Miles</option>
                <option value={DistanceUnit.KILOMETERS}>Kilometers</option>
              </Form.Select>
            </Form.Group>
          </Form>
        </Card.Body>
      </Card>
    </div>
  );
};

export default SettingsPane;
