import React, { useContext } from "react";

import HailTwoToneIcon from "@mui/icons-material/HailTwoTone";
import { AdminPanelSettings } from "@mui/icons-material";
import AccountCircleTwoToneIcon from "@mui/icons-material/AccountCircleTwoTone";
import SmsTwoToneIcon from "@mui/icons-material/SmsTwoTone";
import ExitToAppIcon from "@mui/icons-material/ExitToApp";
import styles from "./Styles/Menu.module.css";
import { ButtonWithIcon } from "./Buttons";
import { AuthContext } from "./AuthProvider";

const userMenuList = [
  [<SmsTwoToneIcon />, "Диалоги", "", 1],
  [<HailTwoToneIcon />, "Люди", "users", 2],
  [<AccountCircleTwoToneIcon />, "Профиль", "profile", 3],
];
const adminMenuList = [
  [<AdminPanelSettings />, "Администрирование", "admin", 4],
  ...userMenuList,
];
const menuVariants = { user: userMenuList, admin: adminMenuList };

export default function Menu() {
  const { logout, user } = useContext(AuthContext);

  return (
    <div className={styles.mainContainer}>
      <div
        style={{
          flex: 3,
          textAlign: "center",
          alignContent: "center",
          minHeight: "120px",
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
          style={{ flex: 1 }}
        />
      ))}
      <div style={{ display: "flex", flex: 12 }}></div>
      <ButtonWithIcon
        onClick={logout}
        icon={<ExitToAppIcon />}
        text={"Выход"}
        style={{ flex: 1 }}
      />
    </div>
  );
}
