import { EmailSharp, EmojiPeopleOutlined } from "@mui/icons-material";
import { DialogsContext } from "../Tabs/DialogsTab";
import React, { memo, useContext, useState } from "react";
import { stringLimit } from "../../Utils";
import styles from "../Styles/DialogCard.module.css";

export const DialogCard = memo(({ dialog }) => {
  const { setCurrentDialog } = useContext(DialogsContext);

  function chooseDialog() {
    dialog.view_status = "viewed";
    setCurrentDialog(dialog);
  }

  return (
    <button className={styles.mainContainer} onClick={chooseDialog}>
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
    </button>
  );
});
