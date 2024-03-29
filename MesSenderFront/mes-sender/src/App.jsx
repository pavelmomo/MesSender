import React, { useState } from "react";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { grey, brown } from "@mui/material/colors";
import Header from "./Components/Header";
import UserView from "./Views/UserView";
import "./index.css";

export const appTheme = createTheme({
  palette: {
    primary: {
      main: brown[300],
      contrast: brown[700],
    },
    secondary: {
      main: grey[50],
      lastMessage: brown[50],
      dialogs: brown[200],
      activeDialog: brown[400],
    },
  },
});

export default function App() {
  const [user, setUser] = useState({ id: 1 });
  return (
    <ThemeProvider theme={appTheme}>
      <UserView user />
    </ThemeProvider>
  );
}
