import { memo } from "react";
import styles from "../Styles/MessageCard.module.css";
import { timeFormat } from "../../Utils";
import { Person2Rounded } from "@mui/icons-material";

export const MessageCard = memo(({ text, isAuthored, dateTime }) => {
  return (
    <div className={styles.messageContainer}>
      <div className={styles.messageIconContainer}>
        {!isAuthored && <Person2Rounded sx={{ margin: 0 }} />}
        {isAuthored && (
          <p style={{ fontSize: 17, fontWeight: "300", margin: 0 }}>Вы</p>
        )}
      </div>
      <p className={styles.messageContent}>{text}</p>
      <p className={styles.timeStyle}>{timeFormat(new Date(dateTime + "Z"))}</p>
    </div>
  );
});
