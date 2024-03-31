import React, { useState } from "react";
import styles from "./Dialog.module.css";
import { ArrowBackIosNewSharp, Person2Rounded } from "@mui/icons-material";
import { IconButton, PushButton } from "../../Buttons/Buttons";
import { TextFieldBase } from "../../TextFields/TextField";

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
  return (
    <div className={styles.dialogContainerStyle}>
      <div style={{ display: "flex", alignItems: "center", height: 70 }}>
        <Person2Rounded sx={{ ml: 3 }}></Person2Rounded>
        <h5 style={{ flex: 1, marginLeft: 15 }}>Jack</h5>
        <IconButton icon={<ArrowBackIosNewSharp sx={{ margin: 2 }} />} />
      </div>

      <div className={styles.messageListContainerStyle}>
        <ul className={styles.messageList}>
          <li>
            <Message
              text="adasdsfdssfdgsdfgbfsdgbdsgrdfsgbdfserfverfvrewevrvwevwrvwrevwervSaafsdfsdfasdsdfasdfsdfsfadfasdfasdfsdfasdf
            fvwerfvwervrevrfvrfvsrfwrevfrevreffbdsfgbregferferva"
            ></Message>
          </li>
          <li>
            <Message
              text="adasdsfdssfdgsdfgbfsdgbdsgrdfsgbdfserfverfvrewevrvwevwrvwrevwervSaafsdfsdfasdsdfasdfsdfsfadfasdfasdfsdfasdf
            fvwerfvwervrevrfvrfvsrfwrevfrevreffbdsfgbregferferva"
            ></Message>
          </li>
          <li>
            <Message
              text="adasdsfdssfdgsdfgbfsdgbdsgrdfsgbdfserfverfvrewevrvwevwrvwrevwervSaafsdfsdfasdsdfasdfsdfsfadfasdfasdfsdfasdf
            fvwerfvwervrevrfvrfvsrfwrevfrevreffbdsfgbregferferva"
            ></Message>
          </li>
          <li>
            <Message
              text="adasdsfdssfdgsdfgbfsdgbdsgrdfsgbdfserfverfvrewevrvwevwrvwrevwervSaafsdfsdfasdsdfasdfsdfsfadfasdfasdfsdfasdf
            fvwerfvwervrevrfvrfvsrfwrevfrevreffbdsfgbregferferva"
            ></Message>
          </li>
          <li>
            <Message text="adasdsa" isAuthored={true}></Message>
          </li>
          <li>
            <Message text="adasdsa"></Message>
          </li>
        </ul>
      </div>

      <div className={styles.inputContainer}>
        <p style={{ margin: 0 }}>Cообщение:</p>
        <TextFieldBase
          style={{ flex: 1, marginLeft: 16, marginRight: 18 }}
          placeholder="Пишите здесь"
        />
        <PushButton text="Отправить"></PushButton>
      </div>
    </div>
  );
}
