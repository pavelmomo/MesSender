import { Box, Card, Grid, List, ListItem } from "@mui/material";
import React, { useState } from "react";
import DialogCard from "./DialogCard";
import { Padding } from "@mui/icons-material";

const dialogStyle = {};

export default function Dialog() {
  return (
    <Box
      sx={{
        display: "flex",
        height: "95%",
        flexDirection: "column",
        padding: 0,
        minWidth: 500,
      }}
    >
      <Box flexBasis="70px" border="2px solid yellow"></Box>
      <Box flexBasis="200px" flexGrow="15" border="2px solid red"></Box>
      <Box flexBasis="70px" border="2px solid black"></Box>
    </Box>
  );
}
