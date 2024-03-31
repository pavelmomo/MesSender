import { EmailSharp, EmojiPeopleOutlined } from "@mui/icons-material";

import React, { useState } from "react";
import { stringLimit } from "../../../Utils";
import styles from "./DialogCard.module.css";

export default function DialogCard({ dialog }) {
  return (
    <div className={styles.mainContainer}>
      <div className={styles.iconContainer}>
        {dialog.view_status === "not_viewed" ? (
          <EmailSharp />
        ) : (
          <EmojiPeopleOutlined />
        )}
      </div>
      <div className={styles.messageContainer}>
        <p style={{ margin: 3 }}>{dialog.dialog_name}</p>
        <h6 className={styles.lastMessage}>
          {stringLimit(dialog.last_message, 30)}
        </h6>
      </div>
    </div>
  );
}
