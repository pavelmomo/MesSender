import React, { useState, useEffect } from "react";
import styles from "../Styles/ProfileTab.module.css";
import { TextFieldBase } from "../Blocks/TextField";
import { PushButton } from "../Blocks/Buttons";
import UserCard from "../Cards/UserCard";

export default function ProfileTab() {
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
      <div className={styles.mainProfileContainer}>
        <h4>Ваш профиль</h4>
      </div>
    </div>
  );
}
