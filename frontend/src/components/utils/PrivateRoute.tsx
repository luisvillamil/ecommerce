import React from "react";
import { Navigate } from "react-router-dom";

const PrivateRoute = ({ auth, children, ...props }) => {
  if (auth.loading || auth.hasAccess) return children;
  return <Navigate to={{ pathname: "/", state: { from: props.location } }} />;
};

export default PrivateRoute;
