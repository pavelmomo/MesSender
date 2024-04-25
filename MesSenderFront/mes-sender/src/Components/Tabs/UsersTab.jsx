import React, { useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import styles from "../Styles/UsersTab.module.css";
import { TextFieldBase } from "../Blocks/TextField";
import { PushButton } from "../Blocks/Buttons";
import { UserCard } from "../Cards/UserCard";
export default function UsersTab() {
  const [users, setUsers] = useState([]);
  const navigate = useNavigate();

  const createDialog = useCallback(async (remote_uid, remote_username) => {
    const dialogStatus = await fetch(
      "/api/dialogs/dual/check?" +
        new URLSearchParams({
          remote_uid: remote_uid,
        }),
      {
        method: "POST",
      }
    ).then(
      (response) => response.json(),
      (error) => console.log(error)
    );
    if (dialogStatus === null) {
      return;
    }
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
  }, []);

  const handleSubmit = useCallback((e) => {
    e.preventDefault();
    fetch(
      "/api/users/all?" +
        new URLSearchParams({
          username: e.target.username.value,
        })
    )
      .then(
        (response) => response.json(),
        (error) => console.log(error)
      )
      .then((data) => setUsers(data));
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
