import React, { useState, useEffect } from "react";
import DialogsList from "../Blocks/DialogList/DialogsList";
import Dialog from "../Blocks/Dialog/Dialog";
import styles from "./Dialogs.module.css";

const EmptyDialog = (
  <div
    style={{
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      height: "100%",
    }}
  >
    <p
      textAlign="center"
      color="var(--main-color)"
      style={{ textAlign: "center", color: "var(--main-color)" }}
    >
      Диалог не выбран
    </p>
  </div>
);

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
    <div className={styles.mainContainer}>
      <div className={styles.dialogListContainer}>
        {dialogs.length && <DialogsList dialogs={dialogs} />}
      </div>
      <div className={styles.mainDialogContainer}>
        <Dialog />
      </div>
    </div>
  );
}
