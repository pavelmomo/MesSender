import { TextFieldBase } from "../TextFields/TextField";
import { PushButton } from "../Buttons";
import { Link, json, useNavigate } from "react-router-dom";
import styles from "../Styles/LoginRegister.module.css";
import { useEffect, useContext } from "react";
import { AuthContext } from "../AuthProvider";
import ModalWindow from "../Blocks/ModalWindow";
import { url } from "../../App";

export default function Login() {
  const { setModalOpen } = useContext(AuthContext);
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    const response = await fetch(`/api/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        username: e.target.username.value,
        password: e.target.password.value,
      }),
    });
    switch (response.status) {
      case 204:
        navigate("/");
        break;
      case 400:
      case 422:
        setModalOpen(true);
        console.log(response);
        break;
      default:
    }
  }
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
      <ModalWindow text="Введены неверные данные" />
    </div>
  );
}
