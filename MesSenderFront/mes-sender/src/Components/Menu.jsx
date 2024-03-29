import React, { useState } from "react";
import MailIcon from "@mui/icons-material/Mail";
import HailTwoToneIcon from "@mui/icons-material/HailTwoTone";
import AccountCircleTwoToneIcon from "@mui/icons-material/AccountCircleTwoTone";
import SmsTwoToneIcon from "@mui/icons-material/SmsTwoTone";
import {
  Drawer,
  ListItemText,
  ListItemButton,
  ListItemIcon,
  Typography,
  List,
  ListItem,
} from "@mui/material/";

const TextStyle = {
  color: "primary.contrast",
};

export default function Menu({ isOpen, setOpen }) {
  const DrawerList = (
    <List sx={{ width: 300 }}>
      <ListItem sx={{ justifyContent: "center", m: 1 }}>
        <Typography variant="h6" sx={TextStyle}>
          Меню
        </Typography>
      </ListItem>
      <ListItem>
        <ListItemButton>
          <ListItemIcon>
            <SmsTwoToneIcon />
          </ListItemIcon>
          <ListItemText primary="Диалоги" sx={TextStyle} />
        </ListItemButton>
      </ListItem>
      <ListItem>
        <ListItemButton>
          <ListItemIcon>
            <HailTwoToneIcon />
          </ListItemIcon>
          <ListItemText primary="Люди" sx={TextStyle} />
        </ListItemButton>
      </ListItem>
      <ListItem>
        <ListItemButton>
          <ListItemIcon>
            <AccountCircleTwoToneIcon />
          </ListItemIcon>
          <ListItemText primary="Профиль" sx={TextStyle} />
        </ListItemButton>
      </ListItem>
    </List>
  );

  return (
    <>
      <Drawer open={isOpen} onClose={() => setOpen(false)}>
        {DrawerList}
      </Drawer>
    </>
  );
}
