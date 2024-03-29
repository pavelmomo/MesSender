import { Box, Card, Grid, List, ListItem } from "@mui/material";
import React, { useState } from "react";
import DialogCard from "./DialogCard";
import { Padding } from "@mui/icons-material";

export default function DialogsList({ dialogs }) {
  return (
    <List>
      {dialogs.map((dialog) => {
        return (
          <ListItem key={dialog.id} disablePadding>
            <DialogCard dialog={dialog} />
          </ListItem>
        );
      })}
    </List>
  );
}
