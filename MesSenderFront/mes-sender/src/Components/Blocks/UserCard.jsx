import styles from "../Styles/UserCard.module.css";
import {
  AccountCircle,
  EmailSharp,
  AssignmentIndOutlined,
} from "@mui/icons-material";

export default function UserCard({ user }) {
  return (
    <div className={styles.mainContainer}>
      <div className={styles.iconContainer}>
        <AssignmentIndOutlined />
      </div>
      <div className={styles.usernameContainer}>
        <p style={{ margin: 3 }}>{user.username}</p>
      </div>
      <button className={styles.iconContainer}>
        <EmailSharp />
      </button>
    </div>
  );
}
