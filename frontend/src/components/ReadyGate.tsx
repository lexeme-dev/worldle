import React from "react";
import { Spinner } from "react-bootstrap";
import { Outlet } from "react-router-dom";
import { useCountries } from "../contexts/CountriesContext";
import { useUser } from "../contexts/UserContext";

const ReadyGate: React.FC = () => {
  const { isLoading: isLoadingCountries } = useCountries();
  const { isLoading: isLoadingUser } = useUser();

  const isLoading = isLoadingCountries || isLoadingUser;

  if (isLoading) {
    return (
      <div className="d-flex justify-content-center py-5">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
      </div>
    );
  }

  return <Outlet />;
};

export default ReadyGate;
