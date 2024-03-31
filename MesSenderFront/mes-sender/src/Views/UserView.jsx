import React, { useState } from "react";
import { Box, Card, Grid, List, ListItem } from "@mui/material";
// import Menu from "../Components/Menu";
import Menu from "../Components/Menu/Menu";
import DialogsTab from "../Components/Tabs/DialogsTab";
import UsersTab from "../Components/Tabs/UsersTab";

export default function UserView({ user }) {
  return (
    <main>
      <div style={{ display: "flex", flexDirection: "row" }}>
        <Menu />
        <DialogsTab />
        {/* <UsersTab></UsersTab> */}
      </div>
    </main>
  );
}
