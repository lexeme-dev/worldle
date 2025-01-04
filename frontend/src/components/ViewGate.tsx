import React from "react";
import { Outlet } from "react-router-dom";
import { ActivePane, useView } from "../contexts/ViewContext";
import SettingsPane from "./SettingsPane";
import StatsPane from "./StatsPane";

const ViewGate: React.FC = () => {
  const { activePane } = useView();

  switch (activePane) {
    case ActivePane.STATS:
      return <StatsPane />;
    case ActivePane.SETTINGS:
      return <SettingsPane />;
    default:
      return <Outlet />;
  }
};

export default ViewGate;
