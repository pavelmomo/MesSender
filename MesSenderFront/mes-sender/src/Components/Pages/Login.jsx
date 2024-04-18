import { TextFieldBase } from "../Blocks/TextField";
import { PushButton } from "../Blocks/Buttons";
import { Link, useNavigate } from "react-router-dom";
import styles from "../Styles/LoginRegister.module.css";
import { useContext, useCallback } from "react";
import { AuthContext } from "../AuthProvider";

export default function Login() {
  const { showModal, login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = useCallback(async (e) => {
    e.preventDefault();
    const stat = await login(e);
    switch (stat) {
      case 204:
        navigate("/");
        break;
      case 400:
      case 422:
        showModal("Введены неверные данные");
        break;
      default:
    }
  }, []);
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
