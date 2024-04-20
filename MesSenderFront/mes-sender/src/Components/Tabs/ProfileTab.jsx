import React, { useState, useContext, useCallback } from "react";
import styles from "../Styles/ProfileTab.module.css";
import { TextFieldBase } from "../Blocks/TextField";
import { PushButton } from "../Blocks/Buttons";
import { AuthContext } from "../AuthProvider";

export default function ProfileTab() {
  const { user, getCurrentUser, showModal } = useContext(AuthContext);
  const [isRowsDisabled, setRowsDisabled] = useState(true);
  const [isSaveDisabled, setSaveDisabled] = useState(true);
  const changeVisability = useCallback(
    (e) => {
      e.preventDefault();
      setRowsDisabled((prev) => !prev);
    },
    [setRowsDisabled]
  );

  const handleSubmit = useCallback(
    async (e) => {
      e.preventDefault();
      const data = {
        email: e.target.email.value,
        username: e.target.username.value,
        password: e.target.password.value,
      };
      if (e.target.new_password.value.trim().length !== 0) {
        data.new_password = e.target.new_password.value;
      }
      const response = await fetch(`/api/users/me`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      switch (response.status) {
        case 201:
          await getCurrentUser();
          e.target.password.value = "";
          setRowsDisabled(true);
          break;
        case 401:
          e.target.password.value = "";
          showModal("Введен неверный пароль");
          break;
        case 422:
          showModal(
            "Введены некорректные данные. Пароль и ник должен быть не менее 4 и не более 20 символов"
          );
          break;
        case 409:
          showModal("Данный ник или почта уже зарегистрированы");
          break;
        default:
      }
    },
    [setRowsDisabled, getCurrentUser, showModal]
  );
  const handlePassChange = useCallback(
    (e) => {
      if (e.target.value !== "" && isSaveDisabled) {
        setSaveDisabled(false);
      } else if (e.target.value === "" && !isSaveDisabled) {
        setSaveDisabled(true);
      }
    },
    [isSaveDisabled]
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
      <form className={styles.mainProfileContainer} onSubmit={handleSubmit}>
        <h4>Профиль пользователя</h4>
        <div className={styles.profileRow}>
          <p style={{ flex: 1 }}>Ваша роль:</p>
          <p style={{ flex: 1 }}>
            {user.role === "moderator" ? "Модератор" : "Пользователь"}
          </p>
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
          <div className={styles.newPassword}>
            <p style={{ flex: 1 }}>Новый пароль:</p>
            <TextFieldBase
              type="password"
              isDisabled={isRowsDisabled}
              name="new_password"
              style={{ flex: 2 }}
              placeholder="Оставьте пустым для сохранения старого пароля"
            ></TextFieldBase>
          </div>
        )}
        {!isRowsDisabled && (
          <div className={styles.profileRow}>
            <p style={{ flex: 1, fontWeight: "500" }}>Пароль:</p>
            <TextFieldBase
              type="password"
              onChange={handlePassChange}
              isDisabled={isRowsDisabled}
              name="password"
              style={{ flex: 2 }}
              placeholder="Обязательное поле"
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
              type="submit"
              text="Сохранить"
              isDisabled={isSaveDisabled}
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
