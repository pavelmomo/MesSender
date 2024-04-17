import React, { useState, useEffect } from "react";
import styles from "../Styles/UsersTab.module.css";
import { TextFieldBase } from "../TextFields/TextField";
import { PushButton } from "../Buttons";
import UserCard from "../Blocks/UserCard";
export default function UsersTab() {
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
        <form className={styles.searchForm}>
          <TextFieldBase
            name="message"
            style={{ flex: 1, marginRight: 14, fontSize: 18 }}
            placeholder="Введите имя пользователя"
          />
          <PushButton type="submit" text="Искать"></PushButton>
        </form>
        <ul className={styles.usersList}>
          <li>
            <UserCard user={{ username: "jack vorobey" }}></UserCard>
          </li>
          <li>
            <UserCard user={{ username: "jack vorobey" }}></UserCard>
          </li>
        </ul>
      </div>
    </div>
  );
}
