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
  return (
    <Box sx={classes.verticalContainer}>
      <Container maxWidth="md">
        <img src={RollingDoodle} />
        <Typography variant="h5" sx={{ fontWeight: 700 }}>
          Welcome back
        </Typography>
        <Typography variant="body1">Log in to navigate your store!</Typography>
        <Stack spacing={3}>
          <TextField size="small" label="User Name" fullWidth />
          <TextField size="small" label="Password" type="password" fullWidth />
        </Stack>
        <Link>Forgot Password?</Link>
        <Button variant="contained" onClick={() => {}}>
          Login
        </Button>
      </Container>
    </Box>
  );
}
