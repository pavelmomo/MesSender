import { TextFieldBase } from "../Blocks/TextField";
import { PushButton } from "../Blocks/Buttons";
import { Link, useNavigate } from "react-router-dom";
import styles from "../Styles/LoginRegister.module.css";
import { useCallback, useContext } from "react";
import { AuthContext } from "../AuthProvider";

export default function Register() {
  const { showModal, register } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = useCallback(async (e) => {
    e.preventDefault();
    const stat = await register(e);
    console.log(stat);
    switch (stat) {
      case 200:
        navigate("/login");
        break;
      case 422:
      case 409:
        showModal(
          "Введены некорректные данные или пользователь уже существует"
        );
        break;
      default:
    }
  }, []);

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
    </div>
  );
}
