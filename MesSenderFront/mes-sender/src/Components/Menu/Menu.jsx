import React, { useState } from "react";

import HailTwoToneIcon from "@mui/icons-material/HailTwoTone";
import AccountCircleTwoToneIcon from "@mui/icons-material/AccountCircleTwoTone";
import SmsTwoToneIcon from "@mui/icons-material/SmsTwoTone";
import ExitToAppIcon from "@mui/icons-material/ExitToApp";
import styles from "./Menu.module.css";
import { ButtonWithIcon } from "../Buttons/Buttons";

export default function Menu() {
  return (
    <div className={styles.mainContainer}>
      <div
        style={{
          flex: 2.5,
          textAlign: "center",
          alignContent: "center",
        }}
      >
        <h5 className={styles.mainLogo}>Me$$ender</h5>
        <h5 className={styles.mainLogo}>¯\_(ツ)_/¯</h5>
      </div>

      <ButtonWithIcon
        icon={<HailTwoToneIcon />}
        text={"Люди"}
        style={{ flex: 1, margin: 1 }}
      />
      <ButtonWithIcon
        icon={<SmsTwoToneIcon />}
        text={"Диалоги"}
        style={{ flex: 1, margin: 1 }}
      />
      <ButtonWithIcon
        icon={<AccountCircleTwoToneIcon />}
        text={"Профиль"}
        style={{ flex: 1, margin: 1 }}
      />
      <div style={{ display: "flex", flex: 11 }}></div>
      <ButtonWithIcon
        icon={<ExitToAppIcon />}
        text={"Выход"}
        style={{ flex: 1, margin: 1 }}
      />
    </div>
  );
}
