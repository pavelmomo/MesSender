import { TextFieldBase } from "../TextFields/TextField";
import { PushButton } from "../Buttons";
import { Link, useNavigate } from "react-router-dom";
import styles from "../Styles/LoginRegister.module.css";
import { useCallback, useContext } from "react";
import { AuthContext } from "../AuthProvider";
import ModalWindow from "../Blocks/ModalWindow";
import { url } from "../../App";

export default function Register() {
  const { setModalOpen } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = useCallback(
    async (e) => {
      e.preventDefault();
      const response = await fetch(`/api/auth/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: e.target.email.value,
          username: e.target.username.value,
          password: e.target.password.value,
        }),
      });
      switch (response.status) {
        case 201:
          navigate("/login");
          break;
        case 400:
        case 422:
          setModalOpen(true);
          break;
        default:
      }
    },
    [navigate, setModalOpen]
  );

  return (
    <div className={styles.mainContainer}>
      <form className={styles.mainForm} onSubmit={handleSubmit}>
        <h3 style={{ textAlign: "center" }}>Регистрация</h3>
        <TextFieldBase
          name="username"
          className={styles.inputFieldRegister}
          placeholder="Имя пользователя"
        ></TextFieldBase>
        <TextFieldBase
          name="email"
          className={styles.inputFieldRegister}
          placeholder="E-mail"
        ></TextFieldBase>
        <TextFieldBase
          name="password"
          type="password"
          className={styles.inputFieldRegister}
          placeholder="Пароль"
        ></TextFieldBase>
        <div style={{ flex: "1", display: "flex" }}>
          <Link className={styles.registerLink} to="/login">
            Уже зарегистрированы?
          </Link>
        </div>
        <PushButton
          type="submit"
          className={styles.submitButton}
          text="Зарегистироваться"
        ></PushButton>
      </form>
      <ModalWindow text="Введены некорректные данные или пользователь уже существует" />
    </div>
  );
}
