import React from "react";
import { Stack } from "react-bootstrap";
import { Github } from "react-bootstrap-icons";
import "./Footer.css";

const Footer: React.FC = () => {
  return (
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
  );
};

export default Footer;
