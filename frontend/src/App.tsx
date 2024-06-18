import React, { useState, useEffect } from "react";
import { HashRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import Login from "./pages/Loging";
import PrivateRoute from "./components/utils/PrivateRoute";
import Dashboard from "./pages/Dashboard";
import { OpenAPI } from "./client";

import { CssBaseline } from "@mui/material";

export default function App() {
  const [auth, setAuth] = useState({ loading: true, hasAccess: false });

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      setAuth((_auth) => ({ ..._auth, loading: false, hasAccess: true }));
    } else {
      setAuth((_auth) => ({ ..._auth, loading: false, hasAccess: false }));
    }
    OpenAPI.TOKEN = token;
  }, []);

  return (
    <>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<Login setAuth={setAuth} />} />
          <Route
            path="/dashboard"
            element={
              <PrivateRoute auth={auth}>
                <Dashboard setAuth={setAuth} />
              </PrivateRoute>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </>
  );
}
