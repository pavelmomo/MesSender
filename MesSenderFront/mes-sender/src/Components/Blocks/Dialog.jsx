import React, { useState, useContext, useRef, useEffect } from "react";
import styles from "../Styles/Dialog.module.css";
import { ArrowBackIosNewSharp, Person2Rounded } from "@mui/icons-material";
import { IconButton, PushButton } from "../Buttons";
import { TextFieldBase } from "../TextFields/TextField";
import { DialogsContext } from "../Tabs/DialogsTab";
import { AuthContext } from "../AuthProvider";

const EmptyDialog = (
  <div className={styles.emptyContainerStyle}>
    <p className={styles.emptyTextStyle}>Диалог не выбран</p>
  </div>
);

function Message({ text, isAuthored }) {
  return (
    <div className={styles.messageContainer}>
      <div className={styles.messageIconContainer}>
        {!isAuthored && <Person2Rounded sx={{ margin: 0 }} />}
        {isAuthored && (
          <p style={{ fontSize: 17, fontWeight: "300", margin: 0 }}>Вы</p>
        )}
      </div>
      <p className={styles.messageContent}>{text}</p>
    </div>
  );
}

export default function Dialog() {
  const [messages, setMessages] = useState([]);
  const messageListContainer = useRef(null);
  const { currentDialog, setCurrentDialog } = useContext(DialogsContext);
  const { user } = useContext(AuthContext);
  useEffect(() => {
    async function loadMessages() {
      const response = await fetch(`/api/dialogs/${currentDialog.id}/messages`);
      if (response.status !== 200) return;
      const mes = await response.json();
      console.log(mes);
      setMessages(mes);
    }
    if (currentDialog !== null) {
      loadMessages();
      messageListContainer.current.scrollTo({
        left: 0,
        top: messageListContainer.current.scrollHeight,
        behavior: "instant",
      });
    }
  }, [currentDialog]);

  async function handleSubmit(e) {
    e.preventDefault();
    const response = await fetch(`/api/dialogs/${currentDialog.id}/messages`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: e.target.message.value,
      }),
    });
    if (response.status === 200) {
      setMessages([
        ...messages,
        { user_id: user.id, text: e.target.message.value },
      ]);
      e.target.message.value = "";
    }
  }

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
            <ul className={styles.messageList}>
              {messages.map((message) => (
                <li key={message.id}>
                  <Message
                    isAuthored={message.user_id === user.id ? true : false}
                    text={message.text}
                  ></Message>
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
