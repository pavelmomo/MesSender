import React, { useState, useEffect, useContext, createContext } from "react";
import DialogsList from "../Blocks/DialogsList";
import Dialog from "../Blocks/Dialog";
import styles from "./DialogsTab.module.css";

export const DialogsContext = createContext(null);

export default function DialogsTab() {
  const [dialogs, setDialogs] = useState([]);
  const [currentDialog, setCurrentDialog] = useState(null);

  useEffect(() => {
    async function loadDialogs() {
      const dialogs = await fetch("/api/dialogs/").then(
        (response) => response.json(),
        () => console.log("Response error!")
      );
      setDialogs(dialogs);
    }
    loadDialogs();
  }, []);

  return (
    <DialogsContext.Provider
      value={{ dialogs, setDialogs, currentDialog, setCurrentDialog }}
    >
      <div className={styles.mainContainer}>
        <div className={styles.dialogListContainer}>
          <DialogsList />
        </div>
        <div className={styles.mainDialogContainer}>
          <Dialog />
        </div>
      </div>
    </DialogsContext.Provider>
  );
}
