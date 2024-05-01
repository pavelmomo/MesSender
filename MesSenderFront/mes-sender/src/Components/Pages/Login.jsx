import { TextFieldBase } from "../TextField";
import { PushButton } from "../Buttons";
import { Link, useNavigate } from "react-router-dom";
import styles from "../Styles/LoginRegister.module.css";
import { useContext, useCallback } from "react";
import { AuthContext } from "../AuthProvider";

export default function Login() {
  const { showModal } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = useCallback(
    async (e) => {
      e.preventDefault();
      try {
        const response = await fetch(`/api/auth/login`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: e.target.username.value,
            password: e.target.password.value,
          }),
        });
        switch (response.status) {
          case 204:
            navigate("/");
            break;
          case 403:
            showModal("Пользователь заблокирован");
            break;
          case 401:
          case 422:
            showModal("Введены неверные данные");
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
    [showModal, navigate]
  );
  return (
    <div className={styles.mainContainer}>
      <form className={styles.mainForm} onSubmit={handleSubmit}>
        <h3 style={{ textAlign: "center" }}>Авторизация</h3>
        <TextFieldBase
          name="username"
          className={styles.inputField}
          placeholder="Имя пользователя"
        ></TextFieldBase>
        <TextFieldBase
          name="password"
          type="password"
          className={styles.inputField}
          style={{ marginBottom: "5px" }}
          placeholder="Пароль"
        ></TextFieldBase>
        <div style={{ flex: "1", display: "flex" }}>
          <Link className={styles.registerLink} to="/register">
            Создать аккаунт?
          </Link>
        </div>
        <PushButton
          type="submit"
          className={styles.submitButton}
          text="Войти"
        ></PushButton>
      </form>
    </div>
  );
}
