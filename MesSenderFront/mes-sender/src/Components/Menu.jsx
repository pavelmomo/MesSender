import React, { useState } from "react";

import HailTwoToneIcon from "@mui/icons-material/HailTwoTone";
import AccountCircleTwoToneIcon from "@mui/icons-material/AccountCircleTwoTone";
import SmsTwoToneIcon from "@mui/icons-material/SmsTwoTone";
import ExitToAppIcon from "@mui/icons-material/ExitToApp";
import {
  Box,
  ListItemText,
  ListItemButton,
  ListItemIcon,
  Typography,
} from "@mui/material/";

const TextStyle = {
  color: "primary.contrast",
};
const ButtonStyle = {
  boxShadow: "0px 1px 3px 0px rgba(99,112,143,0.75)",
  bgcolor: "secondary.lastMessage",
};

export default function Menu({ isOpen, setOpen }) {
  return (
    <Box
      bgcolor={"secondary.menu"}
      sx={{
        display: "flex",
        flexDirection: "column",
        height: "100vh",
        flex: 2,
        boxShadow: "1px 1px 3px 1px rgba(99,112,143,0.75)",
      }}
    >
      <Typography
        variant="h5"
        sx={TextStyle}
        flex={1}
        textAlign={"center"}
        m={3}
      >
        Me$$ender <Box> ¯\_(ツ)_/¯</Box>
      </Typography>

      <Box display="flex" flex={1}>
        <ListItemButton sx={ButtonStyle}>
          <ListItemIcon>
            <HailTwoToneIcon />
          </ListItemIcon>
          <ListItemText primary="Люди" sx={TextStyle} />
        </ListItemButton>
      </Box>
      <Box display="flex" flex={1}>
        <ListItemButton sx={ButtonStyle}>
          <ListItemIcon>
            <SmsTwoToneIcon />
          </ListItemIcon>
          <ListItemText primary="Диалоги" sx={TextStyle} />
        </ListItemButton>
      </Box>
      <Box display="flex" flex={1}>
        <ListItemButton sx={ButtonStyle}>
          <ListItemIcon>
            <AccountCircleTwoToneIcon />
          </ListItemIcon>
          <ListItemText primary="Профиль" sx={TextStyle} />
        </ListItemButton>
      </Box>
      <Box display="flex" flex={11}></Box>
      <Box display="flex" flex={1}>
        <ListItemButton sx={ButtonStyle}>
          <ListItemIcon>
            <ExitToAppIcon />
          </ListItemIcon>
          <ListItemText primary="Выход" sx={TextStyle} />
        </ListItemButton>
      </Box>
    </Box>
  );
}
