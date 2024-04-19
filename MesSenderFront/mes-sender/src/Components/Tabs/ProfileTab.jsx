import React, {
  useState,
  useEffect,
  useContext,
  memo,
  useCallback,
} from "react";
import styles from "../Styles/ProfileTab.module.css";
import { TextFieldBase } from "../Blocks/TextField";
import { PushButton } from "../Blocks/Buttons";
import UserCard from "../Cards/UserCard";
import { AuthContext } from "../AuthProvider";

export default function ProfileTab() {
  const { user } = useContext(AuthContext);
  const [isRowsDisabled, setRowsEnabled] = useState(true);
  const changeVisability = useCallback(
    (e) => {
      e.preventDefault();
      setRowsEnabled((prev) => !prev);
    },
    [setRowsEnabled]
  );

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "row",
        alignItems: "flex-start",
        justifyContent: "center",
        flex: 10,
        width: "100%",
      }}
    >
      <form className={styles.mainProfileContainer}>
        <h4>Профиль пользователя</h4>
        <div className={styles.profileRow}>
          <p style={{ flex: 1 }}>Ваша роль:</p>
          <p style={{ flex: 1 }}>Пользователь</p>
        </div>
        <div className={styles.profileRow}>
          <p style={{ flex: 1 }}>Ваш E-Mail:</p>
          <TextFieldBase
            isDisabled={isRowsDisabled}
            style={{ flex: 1 }}
            name="email"
            defaultValue={user.email}
          ></TextFieldBase>
        </div>
        <div className={styles.profileRow}>
          <p style={{ flex: 1 }}>Ваш уникальный ник:</p>
          <TextFieldBase
            isDisabled={isRowsDisabled}
            name="username"
            style={{ flex: 1 }}
            defaultValue={user.username}
          ></TextFieldBase>
        </div>
        {!isRowsDisabled && (
          <div className={styles.profileRow}>
            <p style={{ flex: 1 }}>Новый пароль:</p>
            <TextFieldBase
              type="password"
              isDisabled={isRowsDisabled}
              name="username"
              style={{ flex: 2 }}
              placeholder="Оставьте пустым для сохранения старого пароля"
            ></TextFieldBase>
          </div>
        )}
        <div style={{ flex: 1 }}></div>
        <div className={styles.profileButtonsRow}>
          <PushButton
            text="Редактировать учётные данные"
            onClick={changeVisability}
            style={{
              height: "50px",
            }}
          />
          {!isRowsDisabled && (
            <PushButton
              text="Сохранить"
              onClick={changeVisability}
              style={{
                height: "50px",
              }}
            />
          )}
        </div>
      </form>
    </div>
  );
}
