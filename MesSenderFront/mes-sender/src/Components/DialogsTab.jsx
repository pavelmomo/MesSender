import { Box, Grid } from "@mui/material";
import React, { useState, useEffect } from "react";
import DialogsList from "./DialogsList";
import Dialog from "./Dialog";

const dialogsGridStyle = {
  height: "90vh",
  minWidth: "370px",
  overflow: "auto",
  mt: 0.8,
  borderRight: "10px auto",
  borderColor: "primary.main",
  "&::-webkit-scrollbar": { display: "none" },
};
const mainDialogGridStyle = {
  height: "85vh",
  margin: 2,
  border: "3px solid",
  borderColor: "secondary.dialogs",
  borderRadius: "10px",
};

export default function DialogsTab() {
  const [dialogs, setDialogs] = useState([]);
  useEffect(() => {
    async function loadDialogs() {
      const url = "http://localhost:8000/api/users/1/dialogs";
      let dialogs = await fetch(url).then(
        (response) => response.json(),
        () => console.log("Response error!")
      );
      setDialogs(dialogs);
    }
    loadDialogs();
  }, []);
  return (
    <Grid
      container
      spacing={1}
      position="relative"
      justifyContent="space-around"
      wrap="nowrap"
    >
      <Grid item xs={4} sx={dialogsGridStyle}>
        {dialogs.length && <DialogsList dialogs={dialogs} />}
      </Grid>
      <Grid item xs={7} sx={mainDialogGridStyle}>
        <Dialog />
      </Grid>
    </Grid>
  );
}
