import React, { useState } from "react";
import { Alert, Button, Card, Form, Modal, Stack } from "react-bootstrap";
import { OverlayTrigger, Tooltip } from "react-bootstrap";
import { Clipboard, InfoCircle } from "react-bootstrap-icons";
import { DistanceUnit, useSettings } from "../contexts/SettingsContext";
import { useUser } from "../contexts/UserContext";

const UUID_REGEX =
  /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

const SettingsPane: React.FC = () => {
  const { distanceUnit, setDistanceUnit } = useSettings();
  const { uuid, changeUserId, validateUserId } = useUser();
  const [showModal, setShowModal] = useState(false);
  const [newUuid, setNewUuid] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isValidating, setIsValidating] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [oldUuid, setOldUuid] = useState<string | null>(null);

  const copyUuid = () => {
    if (uuid) {
      navigator.clipboard.writeText(uuid);
    }
  };

  const handleChangeUserId = async () => {
    if (!UUID_REGEX.test(newUuid)) {
      setError("Please enter a valid user ID.");
      return;
    }

    setIsValidating(true);
    setError(null);

    try {
      const isValid = await validateUserId(newUuid);
      if (!isValid) {
        setError("This User ID does not exist");
        return;
      }

      setOldUuid(uuid);
      await changeUserId(newUuid);
      setShowModal(false);
      setSuccessMessage("User ID changed successfully");
    } catch (e) {
      setError("Failed to change User ID");
    } finally {
      setIsValidating(false);
    }
  };

  const isSameUuid = newUuid === uuid;
  const isValidFormat = UUID_REGEX.test(newUuid);

  const getChangeButton = (inModal: boolean) => {
    const button = (
      <Button
        variant={inModal ? "primary" : "outline-secondary"}
        size="sm"
        onClick={inModal ? handleChangeUserId : () => setShowModal(true)}
        disabled={
          inModal ? isValidating || isSameUuid || !isValidFormat : isSameUuid
        }
      >
        {inModal ? (isValidating ? "Validating..." : "Change") : "Change"}
      </Button>
    );

    if (
      (inModal && (!isValidFormat || isSameUuid)) ||
      (!inModal && isSameUuid)
    ) {
      return (
        <OverlayTrigger
          placement="right"
          overlay={
            <Tooltip>
              {isSameUuid
                ? "This is your current User ID"
                : "Please enter a valid user ID"}
            </Tooltip>
          }
        >
          <span>{button}</span>
        </OverlayTrigger>
      );
    }

    return button;
  };

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
          <hr className="my-4" />
          <Stack gap={2} className="align-items-center">
            {successMessage && oldUuid && (
              <Alert
                variant="success"
                dismissible
                onClose={() => {
                  setSuccessMessage(null);
                  setOldUuid(null);
                }}
              >
                <Alert.Heading>{successMessage}</Alert.Heading>
                <p className="mb-0">
                  Your previous User ID was: <code>{oldUuid}</code>
                </p>
              </Alert>
            )}
            <div className="d-flex align-items-center gap-2">
              <span>Your User ID</span>
              <OverlayTrigger
                placement="right"
                overlay={
                  <Tooltip>
                    Your unique identifier used to track your game progress
                  </Tooltip>
                }
              >
                <InfoCircle className="text-muted" />
              </OverlayTrigger>
            </div>
            <div className="d-flex gap-2 align-items-center">
              <Form.Control
                type="text"
                value={uuid}
                readOnly
                className="text-monospace"
                style={{ width: "auto" }}
              />
              <Button
                variant="outline-secondary"
                size="sm"
                onClick={copyUuid}
                title="Copy to clipboard"
              >
                <Clipboard />
              </Button>
              {getChangeButton(false)}
            </div>
          </Stack>
        </Card.Body>
      </Card>

      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Change User ID</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p>
            Changing your User ID will set your game progress and statistics to
            those of the provided user. Only do this if you want to transfer
            your game progress from another device.
          </p>
          <Form.Group className="mb-3">
            <Form.Label>New User ID</Form.Label>
            <Form.Control
              type="text"
              value={newUuid}
              onChange={(e) => setNewUuid(e.target.value)}
              isInvalid={!!error}
            />
            <Form.Control.Feedback type="invalid">
              {error}
            </Form.Control.Feedback>
          </Form.Group>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Cancel
          </Button>
          {getChangeButton(true)}
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default SettingsPane;
