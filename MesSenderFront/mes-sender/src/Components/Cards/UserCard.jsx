import styles from "../Styles/UserCard.module.css";
import { memo, useContext } from "react";
import { AuthContext } from "../AuthProvider";
import { EmailSharp, AssignmentIndOutlined } from "@mui/icons-material";

export const UserCard = memo(({ cardUser, createDialog }) => {
  const { user } = useContext(AuthContext);
  return (
    <div className={styles.mainContainer}>
      <div className={styles.iconContainer}>
        <AssignmentIndOutlined />
      </div>
      <div className={styles.usernameContainer}>
        <p style={{ margin: 3 }}>{cardUser.username}</p>
      </div>
      {cardUser.id !== user.id && (
        <button
          className={styles.iconContainer}
          onClick={() => createDialog(cardUser.id)}
        >
          <EmailSharp />
        </button>
      )}
    </div>
  );
});
