import { memo } from "react";
import styles from "../Styles/MessageCard.module.css";
import { ArrowBackIosNewSharp, Person2Rounded } from "@mui/icons-material";

export const MessageCard = memo(({ text, isAuthored }) => {
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
});
