import styles from "../Styles/AdminUserCard.module.css";
import { memo } from "react";

export const AdminUserCard = memo(({ cardUser, banUser }) => {
  return (
    <div className={styles.mainContainer}>
      <div className={styles.dataContainer}>
        <p style={{ margin: 3 }}>
          {cardUser.role === "user"
            ? "Пользователь " + cardUser.username
            : "Администратор " + cardUser.username}
        </p>
      </div>
      {cardUser.role !== "admin" && (
        <div style={{ display: "flex", textAlign: "center" }}>
          <p>Статус: </p>
          {!cardUser.is_banned ? (
            <button
              className={styles.statusContainer}
              onClick={() => banUser(cardUser.id, true)}
              title="Заблокировать"
            >
              Активен
            </button>
          ) : (
            <button
              className={styles.statusContainer}
              onClick={() => banUser(cardUser.id, false)}
              title="Разблокировать"
            >
              Заблокирован
            </button>
          )}
        </div>
      )}
    </div>
  );
});
