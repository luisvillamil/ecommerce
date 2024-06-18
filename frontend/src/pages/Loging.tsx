import React, { useState } from "react";
import RollingDoodle from "../assets/RollingDoodle.svg";
import { Box, Button, Container, Link, Stack, TextField, Typography } from "@mui/material";
import { LoginService } from ".././client";

const classes = {
  verticalContainer: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    minHeight: "100vh",
  },
};

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    const response = await LoginService.getAccessToken({
      formData: {
        username: username,
        password: password,
      },
    });
    console.log(response);
    // localStorage.setItem('access_token', response.access_token)
  };

  return (
    <Box sx={{ px: 1, py: 6 }}>
      <Container maxWidth="md">
        <Box>
          <img src={RollingDoodle} />
        </Box>

        <Stack spacing={1} sx={{ mb: 5 }}>
          <Typography variant="h5" sx={{ fontWeight: 700, color: "#7fbbca" }}>
            Welcome back
          </Typography>
          <Typography variant="subtitle1">Log in to navigate your store!</Typography>
        </Stack>

        <Stack spacing={3}>
          <TextField
            size="small"
            label="User Name"
            fullWidth
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <TextField
            size="small"
            label="Password"
            type="password"
            fullWidth
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </Stack>
        <Box sx={{ textAlign: "right", mt: 1 }}>
          <Link>Forgot Password?</Link>
        </Box>

        <Box sx={{ width: "100%", mt: 4 }}>
          <Button sx={{ textTransform: "none", fontSize: "1rem" }} variant="contained" onClick={handleLogin} fullWidth>
            Login
          </Button>
        </Box>
      </Container>
    </Box>
  );
}
