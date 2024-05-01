import React, { useState, useCallback, useContext } from "react";
import { useNavigate } from "react-router-dom";
import styles from "../Styles/UsersTab.module.css";
import { TextFieldBase } from "../TextField";
import { PushButton } from "../Buttons";
import { UserCard } from "../Cards/UserCard";
import { AuthContext } from "../AuthProvider";

export default function UsersTab() {
  const [users, setUsers] = useState([]);
  const { showModal } = useContext(AuthContext);
  const navigate = useNavigate();

  const createDialog = useCallback(async (remote_uid, remote_username) => {
    try {
      const response = await fetch(
        "/api/dialogs/dual/check?" +
          new URLSearchParams({
            remote_uid: remote_uid,
          }),
        { method: "POST" }
      );
      switch (response.status) {
        case 200:
          const dialogStatus = await response.json();
          if (dialogStatus.is_exist) {
            navigate(
              `/dialogs?` +
                new URLSearchParams({
                  exist_dialog_id: dialogStatus.dialog_id,
                  dialog_name: remote_username,
                })
            );
          } else {
            navigate(
              `/dialogs?` +
                new URLSearchParams({
                  dialog_name: remote_username,
                  remote_uid: remote_uid,
                })
            );
          }
          break;
        case 401:
        case 403:
          navigate("/login");
          break;
        default:
          throw Error(
            "Ошибка при обращении к серверу.Статус ответа: " + response.status
          );
      }
    } catch (err) {
      console.log(err);
      showModal("Произошла ошибка при обращении к серверу");
    }
  }, []);

  const handleSubmit = useCallback(async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(
        "/api/users/search?" +
          new URLSearchParams({
            username: e.target.username.value,
          })
      );
      switch (response.status) {
        case 200:
          setUsers(await response.json());
          break;
        case 401:
        case 403:
          navigate("/login");
          break;
        default:
          throw Error(
            "Ошибка при обращении к серверу.Статус ответа: " + response.status
          );
      }
    } catch (err) {
      console.log(err);
      showModal("Произошла ошибка при обращении к серверу");
    }
  }, []);

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
      <div className={styles.mainUsersContainer}>
        <h4>Поиск пользователей</h4>
        <form className={styles.searchForm} onSubmit={handleSubmit}>
          <TextFieldBase
            name="username"
            style={{ flex: 1, marginRight: 14, fontSize: 18 }}
            placeholder="Введите имя пользователя"
          />
          <PushButton type="submit" text="Искать"></PushButton>
        </form>
        <ul className={styles.usersList}>
          {users != null &&
            users.map((user) => (
              <li key={user.id}>
                <UserCard
                  cardUser={user}
                  createDialog={createDialog}
                ></UserCard>
              </li>
            ))}
        </ul>
      </div>
    </div>
  );
}
