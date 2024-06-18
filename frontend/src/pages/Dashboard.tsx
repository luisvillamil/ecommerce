import React from "react";
import { Link } from "@mui/material";

export default function Dashboard(props) {
  const handleLogout = () => {
    props.setAuth((_auth) => ({ ..._auth, hasAccess: false }));
    localStorage.removeItem("access_token");
  };

  return (
    <>
      <h1>Dashboard Page</h1>
      <Link onClick={handleLogout}>Logout</Link>
    </>
  );
}
