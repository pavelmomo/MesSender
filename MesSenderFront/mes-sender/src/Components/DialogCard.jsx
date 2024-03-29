import {
  EmailSharp,
  LabelSharp,
  FiberManualRecordSharp,
} from "@mui/icons-material";
import { Box, Grid, List, ListItem, Typography } from "@mui/material";
import React, { useState } from "react";
import { stringLimit } from "../Utils";
const CardStyle = {
  width: "100%",
  height: "80px",
  marginLeft: 1,
  marginBottom: 2,
  display: "flex",
  border: "2px solid",
  borderColor: "secondary.dialogs",
  borderRadius: "8px",
};

const LastMessageStyle = {
  width: 250,
  paddingLeft: 1,
  paddingTop: 0.5,
  paddingRight: 1,
  bgcolor: "secondary.lastMessage",
  borderRadius: 2,
};

export default function DialogCard({ dialog }) {
  return (
    <Box sx={CardStyle}>
      <Box sx={{ flexBasis: "70px" }} textAlign="center" alignSelf="center">
        {dialog.view_status === "not_viewed" ? (
          <EmailSharp />
        ) : (
          <FiberManualRecordSharp />
        )}
      </Box>
      <Box sx={{ padding: 1.3, display: "flex", flexDirection: "column" }}>
        <Typography variant="body1">{dialog.dialog_name}</Typography>
        <Typography variant="caption" sx={LastMessageStyle}>
          {stringLimit(dialog.last_message, 30)}
        </Typography>
      </Box>
    </Box>
  );
}
