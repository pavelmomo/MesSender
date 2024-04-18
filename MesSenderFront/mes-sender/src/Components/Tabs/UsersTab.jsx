import React, { useState, useEffect, useCallback } from "react";
import styles from "../Styles/UsersTab.module.css";
import { TextFieldBase } from "../Blocks/TextField";
import { PushButton } from "../Blocks/Buttons";
import { UserCard } from "../Cards/UserCard";
export default function UsersTab() {
  const [users, setUsers] = useState([]);

  const createDialog = useCallback(async (remote_uid) => {
    const dialogStatus = await fetch("/api/dialogs/dual", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        remote_uid: remote_uid,
      }),
    }).then(
      (response) => response.json(),
      (error) => console.log(error)
    );
    if (dialogStatus === null) {
      return;
    }
    switch (dialogStatus.status) {
      case "created":
        break;
      case "existed":
        alert("dialog exist");
        break;
      default:
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
