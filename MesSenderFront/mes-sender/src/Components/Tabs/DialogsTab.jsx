import DialogsList from "../Blocks/DialogsList";
import { useSearchParams } from "react-router-dom";
import Dialog from "../Blocks/Dialog";
import styles from "../Styles/DialogsTab.module.css";
import { AuthContext } from "../AuthProvider";
import { wsUri } from "../../Utils";

import React, {
  useState,
  useEffect,
  useContext,
  createContext,
  useCallback,
} from "react";

export const DialogsContext = createContext(null);

export default function DialogsTab() {
  const { user } = useContext(AuthContext);
  const [messages, setMessages] = useState([]);
  const [dialogs, setDialogs] = useState([]);
  const [currentDialog, setCurrentDialog] = useState(null);
  const [dialogWS, setDialogWS] = useState(null);
  const [searchParams, setSearchParams] = useSearchParams();

  const loadDialogs = useCallback(async () => {
    var dialogsBuf = await fetch(`/api/dialogs/`).then(
      (response) => response.json(),
      () => console.log("Response error!")
    );
    dialogsBuf = dialogsBuf !== null ? dialogsBuf : [];
    const dialog_id = searchParams.get("dialog_id");
    if (dialog_id != null) {
      const dialog_ind = dialogsBuf.findIndex(
        (e) => e.id === Number(dialog_id)
      );
      if (dialog_ind !== -1) {
        setCurrentDialog(dialogsBuf[dialog_ind]);
      }
    }
    setSearchParams({});
    setDialogs(dialogsBuf);
  }, []);

  const handleNewMessage = useCallback(
    (e) => {
      const recvPacket = JSON.parse(JSON.parse(e.data));

      if (recvPacket.event === "send_message") {
        //получено новое сообщение
        const dialogIndex = dialogs.findIndex(
          (item) => item.id === recvPacket.data.dialog_id
        );

        if (dialogIndex !== -1) {
          //проверка на существование диалога
          const bufDialog = dialogs[dialogIndex];
          bufDialog.last_message = recvPacket.data.text;

          if (
            currentDialog !== null &&
            currentDialog.id === recvPacket.data.dialog_id
          ) {
            //открыт диалог с пользователем, приславшим сообщение
            setMessages((prev) => [...prev, recvPacket.data]);
            //высылаем для сообщения статус - прочтено
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
          //загрузка всех диалогов, поскольку сообщение из нового диалога
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
          const bufElem = element;
          if (
            recvPacket.data.message_ids.findIndex((e) => e === element.id) !==
            -1
          ) {
            bufElem.status = "viewed";
          }
          return bufElem;
        });
        setMessages(bufMessages);
      }
    },
    [currentDialog, dialogs, dialogWS, user, messages, loadDialogs]
  );
  useEffect(() => {
    loadDialogs();
    const ws = new WebSocket(`${wsUri}/api/messages/ws`);
    setDialogWS(ws);
    return () => ws.close();
  }, [loadDialogs]);

  useEffect(() => {
    if (dialogWS !== null) {
      dialogWS.onmessage = handleNewMessage;
    }
  }, [dialogWS, handleNewMessage]);

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
