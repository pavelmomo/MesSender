import React, { useState, useCallback, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import styles from "../Styles/AdminTab.module.css";
import { AdminUserCard } from "../Cards/AdminUserCard";
import { AuthContext } from "../AuthProvider";

export default function AdminTab() {
  const [users, setUsers] = useState([]);
  const { showModal } = useContext(AuthContext);
  const navigate = useNavigate();

  const loadUsers = useCallback(async () => {
    try {
      const response = await fetch("/api/users/all");
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
  }, [setUsers, showModal, navigate]);

  useEffect(() => {
    loadUsers();
  }, []);

  const banUser = useCallback(
    async (user_id, banStatus) => {
      try {
        const response = await fetch(
          `/api/users/${user_id}?` +
            new URLSearchParams({
              is_banned: banStatus,
            }),
          { method: "PATCH" }
        );
        switch (response.status) {
          case 204:
            await loadUsers();
            const messageStat = banStatus ? "заблокирован" : "разблокирован";
            showModal("Пользователь успешно " + messageStat);
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
    },
    [loadUsers, showModal, navigate]
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
      <div className={styles.mainUsersContainer}>
        <h4>Панель администратора</h4>
        <ul className={styles.usersList}>
          {users != null &&
            users.map((user) => (
              <li key={user.id}>
                <AdminUserCard
                  cardUser={user}
                  banUser={banUser}
                ></AdminUserCard>
              </li>
            ))}
        </ul>
      </div>
    </div>
  );
}
