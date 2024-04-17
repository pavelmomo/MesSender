import React, { useState, useEffect, useContext, createContext } from "react";
import DialogsList from "../Blocks/DialogsList";
import Dialog from "../Blocks/Dialog";
import styles from "./DialogsTab.module.css";
import { AuthContext } from "../AuthProvider";
import { wsUri } from "../../Utils";
export const DialogsContext = createContext(null);

export default function DialogsTab() {
  const { user } = useContext(AuthContext);
  const [messages, setMessages] = useState([]);
  const [dialogs, setDialogs] = useState([]);
  const [currentDialog, setCurrentDialog] = useState(null);
  const [dialogWS, setDialogWS] = useState(null);

  function handleNewMessage(e) {
    const recvPacket = JSON.parse(JSON.parse(e.data));

    if (recvPacket.event === "send_message") {
      const dialogIndex = dialogs.findIndex(
        (item) => item.id === recvPacket.data.dialog_id
      );

      if (dialogIndex !== -1) {
        const bufDialog = dialogs[dialogIndex];
        bufDialog.last_message = recvPacket.data.text;

        if (
          currentDialog !== null &&
          currentDialog.id === recvPacket.data.dialog_id
        ) {
          //открыт диалог с пользователем, приславшим сообщение
          setMessages([...messages, recvPacket.data]);
          if (recvPacket.data.user_id !== user.id) {
            dialogWS.send(
              JSON.stringify({
                event: "set_message_viewed",
                data: {
                  message_ids: [recvPacket.data.id],
                  dialog_id: recvPacket.data.dialog_id,
                },
              })
            );
          }

          //высылаем для сообщения статус - прочтено
        } else {
          //диалог с пользователем не открыт
          if (recvPacket.data.user_id !== user.id) {
            bufDialog.view_status = "not_viewed";
          }
        }
        const bufDialogs = [...dialogs];
        bufDialogs.splice(dialogIndex, 1);
        bufDialogs.unshift(bufDialog);
        setDialogs(bufDialogs);
      } else {
        loadDialogs();
      }
    } else if (recvPacket.event === "set_message_viewed") {
      //отметка на сообщениях - прочтено
      if (
        currentDialog == null ||
        currentDialog.id !== recvPacket.data.dialog_id
      ) {
        return;
      }
      const bufMessages = messages.map((element) => {
        if (
          recvPacket.data.message_ids.findIndex((e) => e === element.id) !== -1
        ) {
          element.status = "viewed";
        }
        return element;
      });
      setMessages(bufMessages);
    }
  }
  console.log("rendeer");
  async function loadDialogs() {
    const dialogs = await fetch(`/api/dialogs/`).then(
      (response) => response.json(),
      () => console.log("Response error!")
    );
    setDialogs(dialogs);
    console.log(dialogs);
  }

  useEffect(() => {
    loadDialogs();
    const ws = new WebSocket(`${wsUri}/api/messages/ws`);
    setDialogWS(ws);
    return () => ws.close();
  }, []);

  useEffect(() => {
    if (dialogWS !== null) {
      dialogWS.onmessage = handleNewMessage;
    }
  }, [currentDialog, dialogs, dialogWS, messages]);

  return (
    <DialogsContext.Provider
      value={{
        dialogs,
        setDialogs,
        currentDialog,
        setCurrentDialog,
        dialogWS,
        messages,
        setMessages,
      }}
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
