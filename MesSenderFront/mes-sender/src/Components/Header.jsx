import MenuIcon from "@mui/icons-material/Menu";
import { useState } from "react";
import Menu from "./Menu";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
} from "@mui/material/";

export default function Header({ setMenuOpen }) {
  return (
    <>
      <header>
        <AppBar position="relative" sx={{ mb: 2 }}>
          <Toolbar>
            <IconButton
              size="large"
              edge="start"
              color="inherit"
              sx={{ mr: 2 }}
              onClick={() => setMenuOpen(true)}
            >
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Диалоги
            </Typography>
            <Button color="inherit">Выйти</Button>
          </Toolbar>
        </AppBar>
      </header>
    </>
  );
}
