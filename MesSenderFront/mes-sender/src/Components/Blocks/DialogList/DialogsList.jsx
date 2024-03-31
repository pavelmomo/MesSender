import { Box, Card, Grid, List, ListItem } from "@mui/material";
import React, { useState } from "react";
import DialogCard from "../DialogCard/DialogCard";

export default function DialogsList({ dialogs }) {
  return (
    <ul style={{ listStyle: "none" }}>
      {dialogs.map((dialog) => {
        return (
          <li key={dialog.id}>
            <DialogCard dialog={dialog} />
          </li>
        );
      })}
    </ul>
  );
}
