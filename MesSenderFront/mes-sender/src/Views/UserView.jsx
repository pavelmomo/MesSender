import React, { useState } from "react";
import Header from "../Components/Header";
import Menu from "../Components/Menu";
import DialogsTab from "../Components/DialogsTab";

export default function UserView({ user }) {
  const [isMenuOpen, setMenuOpen] = useState(false);
  return (
    <main>
      <Header setMenuOpen={setMenuOpen} />
      <DialogsTab />
      <Menu isOpen={isMenuOpen} setOpen={setMenuOpen} />
    </main>
  );
}
