import React, { useContext, useState } from "react";

import HailTwoToneIcon from "@mui/icons-material/HailTwoTone";
import AccountCircleTwoToneIcon from "@mui/icons-material/AccountCircleTwoTone";
import SmsTwoToneIcon from "@mui/icons-material/SmsTwoTone";
import ExitToAppIcon from "@mui/icons-material/ExitToApp";
import styles from "../Styles/Menu.module.css";
import { ButtonWithIcon } from "../Buttons";
import { AuthContext } from "../AuthProvider";

const userMenuList = [
  [<SmsTwoToneIcon />, "Диалоги", "", 1],
  [<HailTwoToneIcon />, "Люди", "users", 2],
  [<AccountCircleTwoToneIcon />, "Профиль", "profile", 3],
];
const moderatorMenuList = [[<HailTwoToneIcon />, "Жалобы", "hhh", 4]];
const menuVariants = { user: userMenuList, moderator: moderatorMenuList };

export default function Menu() {
  const { logout, user } = useContext(AuthContext);

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
      {menuVariants[user.role].map((item) => (
        <ButtonWithIcon
          key={item[3]}
          icon={item[0]}
          text={item[1]}
          linkPath={item[2]}
          style={{ flex: 1, margin: 1 }}
        />
      ))}
      <div style={{ display: "flex", flex: 12 }}></div>
      <ButtonWithIcon
        onClick={logout}
        icon={<ExitToAppIcon />}
        text={"Выход"}
        style={{ flex: 1, margin: 1 }}
      />
    </div>
  );
}
