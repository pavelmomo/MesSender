import { Box, Card, Grid, List, ListItem } from "@mui/material";
import React, { useContext, useState } from "react";
import DialogCard from "./DialogCard";
import { DialogsContext } from "../Tabs/DialogsTab";

const emptyList = (
  <h6
    style={{
      textAlign: "center",
      marginTop: "10%",
      color: "var(--main-color)",
      fontWeight: "400",
    }}
  >
    Активных диалогов нет
  </h6>
);

export default function DialogsList() {
  const { dialogs } = useContext(DialogsContext);

  return (
    <>
      {dialogs.length !== 0 ? (
        <ul style={{ listStyle: "none" }}>
          {dialogs.map((dialog) => (
            <li key={dialog.id}>
              <DialogCard dialog={dialog} />
            </li>
          ))}
        </ul>
      ) : (
        emptyList
      )}
    </>
  );
}
