import React, { useCallback, useContext, useRef, useEffect } from "react";
import { MessageCard } from "../Cards/MessageCard";
import styles from "../Styles/Dialog.module.css";
import { ArrowBackIosNewSharp, Person2Rounded } from "@mui/icons-material";
import { IconButton, PushButton } from "./Buttons";
import { TextFieldBase } from "./TextField";
import { DialogsContext } from "../Tabs/DialogsTab";
import { AuthContext } from "../AuthProvider";

const EmptyDialog = (
  <div className={styles.emptyContainerStyle}>
    <p className={styles.emptyTextStyle}>Диалог не выбран</p>
  </div>
);

export default function Dialog() {
  const messageListContainer = useRef(null);
  const { currentDialog, setCurrentDialog, messages, setMessages, dialogWS } =
    useContext(DialogsContext);
  const { user } = useContext(AuthContext);

  useEffect(() => {
    async function loadMessages() {
      const response = await fetch(`/api/dialogs/${currentDialog.id}/messages`);
      if (response.status !== 200) return;
      const mes = await response.json();
      setMessages(mes);
    }
    if (
      currentDialog !== null &&
      currentDialog.id !== null &&
      !currentDialog.hasOwnProperty("no_need_load")
    ) {
      loadMessages();
      messageListContainer.current.scrollTo({
        left: 0,
        top: messageListContainer.current.scrollHeight,
        behavior: "instant",
      });
    }
  }, [currentDialog, setMessages]);

  useEffect(() => {
    if (currentDialog !== null) {
      messageListContainer.current.scrollTo({
        left: 0,
        top: messageListContainer.current.scrollHeight,
        behavior: "instant",
      });
    }
  }, [messages, currentDialog]);

  const handleSubmit = useCallback(
    async (e) => {
      e.preventDefault();
      if (dialogWS == null || e.target.message.value.trim().length === 0) {
        return;
      }
      if (
        // диалог является новым, на сервере его еще не существует
        currentDialog.id == null
      ) {
        const responseData = await fetch("/api/dialogs/dual", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            remote_uid: currentDialog.remote_uid,
          }),
        }).then(
          (response) => response.json(),
          (error) => console.log(error)
        );
        // создан новый диалог на сервере, устанавливаем id
        setCurrentDialog((prev) => {
          return {
            id: responseData.dialog_id,
            dialog_name: prev.dialog_name,
            no_need_load: true,
          };
        });
        dialogWS.send(
          JSON.stringify({
            event: "send_message",
            data: {
              dialog_id: responseData.dialog_id,
              text: e.target.message.value,
            },
          })
        );
      } else {
        // обычная отправка сообщения
        dialogWS.send(
          JSON.stringify({
            event: "send_message",
            data: {
              dialog_id: currentDialog.id,
              text: e.target.message.value,
            },
          })
        );
      }
      e.target.message.value = "";
    },
    [dialogWS, currentDialog]
  );

  return (
    <>
      {currentDialog === null ? (
        EmptyDialog
      ) : (
        <div className={styles.dialogContainerStyle}>
          <div style={{ display: "flex", alignItems: "center", height: 70 }}>
            <Person2Rounded sx={{ ml: 3 }}></Person2Rounded>
            <h5 style={{ flex: 1, marginLeft: 15 }}>
              {currentDialog.dialog_name}
            </h5>
            <IconButton
              onClick={() => setCurrentDialog(null)}
              icon={<ArrowBackIosNewSharp sx={{ margin: 2 }} />}
            />
          </div>

          <div
            className={styles.messageListContainerStyle}
            ref={messageListContainer}
          >
            <ul className={styles.messageList} style={{ width: "100%" }}>
              {messages.map((message) => (
                <li
                  key={message.id}
                  style={{
                    borderRadius: "5px",
                    width: "100%",
                    margin: "5px",
                    backgroundColor:
                      message.status === "viewed"
                        ? "var(--secondary-color)"
                        : "var(--main-light-color)",
                  }}
                >
                  <MessageCard
                    dateTime={message.created_at}
                    isAuthored={message.user_id === user.id ? true : false}
                    text={message.text}
                  ></MessageCard>
                </li>
              ))}
            </ul>
          </div>

          <form className={styles.inputContainer} onSubmit={handleSubmit}>
            <p style={{ margin: 0 }}>Cообщение:</p>
            <TextFieldBase
              name="message"
              style={{ flex: 1, marginLeft: 16, marginRight: 18 }}
              placeholder="Пишите здесь"
            />
            <PushButton type="submit" text="Отправить"></PushButton>
          </form>
        </div>
      )}
    </>
  );
}
