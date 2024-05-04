import DialogsList from "../DialogsList";
import { useNavigate, useSearchParams } from "react-router-dom";
import Dialog from "../Dialog";
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
  const { user, showModal } = useContext(AuthContext);
  const [messages, setMessages] = useState([]);
  const [dialogs, setDialogs] = useState([]);
  const navigate = useNavigate();
  const [currentDialog, setCurrentDialog] = useState(null);
  const [dialogWS, setDialogWS] = useState(null);
  const [searchParams, setSearchParams] = useSearchParams();

  const loadDialogs = useCallback(async () => {
    var dialogsBuf = [];
    try {
      const response = await fetch(`/api/dialogs/`);
      switch (response.status) {
        case 200:
          dialogsBuf = await response.json();
          break;
        case 401:
        case 403:
          navigate("/login");
          break;
        default:
          throw Error(
            "Ошибка при обращении к серверу.Статус ответа: " + response.status
          );
      }
    } catch (err) {
      console.log(err);
      showModal("Произошла ошибка при обращении к серверу");
      return;
    }
    const dialogName = searchParams.get("dialog_name");

    if (dialogName !== null) {
      // была переадресация со страницы поиска пользователей
      const dialogId = searchParams.get("exist_dialog_id");
      if (dialogId !== null) {
        // переадресация на существующий диалог
        setCurrentDialog({ id: Number(dialogId), dialog_name: dialogName });
      } else {
        // диалог еще не существует
        const remoteUid = searchParams.get("remote_uid");
        if (remoteUid !== null) {
          setCurrentDialog({
            dialog_name: dialogName,
            remote_uid: Number(remoteUid),
            id: null,
          });
        }
      }

      setSearchParams({});
    }

    setDialogs(dialogsBuf);
  }, [searchParams, setSearchParams, setCurrentDialog, showModal, navigate]);

  const handleNewMessage = useCallback(
    (e) => {
      const recvPacket = JSON.parse(JSON.parse(e.data));
      if (recvPacket.event === "send_message") {
        //получено новое сообщение
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
        }
        const dialogIndex = dialogs.findIndex(
          (item) => item.id === recvPacket.data.dialog_id
        );

        //диалог, в котороый пришло собщение, есть в списке диалогов
        if (dialogIndex !== -1) {
          const bufDialog = dialogs[dialogIndex];
          bufDialog.last_message = recvPacket.data.text;
          // смена статуса диалога (смена иконки)
          if (recvPacket.data.user_id !== user.id) {
            // открыт диалог, в который пришло сообщение - не меняем статус
            if (currentDialog !== null && currentDialog.id === bufDialog.id) {
              bufDialog.view_status = "viewed";
            } else {
              bufDialog.view_status = "not_viewed";
            }
          }
          //пересортировка диалогов
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
    try {
      const ws = new WebSocket(`${wsUri}/api/messages/ws`);
      ws.onclose = (e) => {
        switch (e.code) {
          case 1008:
            navigate("/login");
            break;
          case 1012:
            showModal(
              "Произошло отключение от сервера. Попробуйте перезагузить страницу"
            );
            break;
          default:
        }
      };

      setDialogWS(ws);
      return () => ws.close();
    } catch (err) {
      console.log(err);
    }
  }, []);

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
