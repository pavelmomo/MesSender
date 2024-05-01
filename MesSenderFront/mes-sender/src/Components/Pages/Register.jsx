import { TextFieldBase } from "../TextField";
import { PushButton } from "../Buttons";
import { Link, useNavigate } from "react-router-dom";
import styles from "../Styles/LoginRegister.module.css";
import { useCallback, useContext } from "react";
import { AuthContext } from "../AuthProvider";

export default function Register() {
  const { showModal } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = useCallback(
    async (e) => {
      e.preventDefault();
      try {
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
          case 200:
            showModal("Вы успешно зарегистрированы");
            navigate("/login");
            break;
          case 422:
            showModal(
              "Введены некорректные данные. Пароль и ник должен быть не менее 4 и не более 20 символов"
            );
            break;
          case 409:
            showModal(
              "Введены некорректные данные или пользователь уже существует"
            );
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
    [navigate, showModal]
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
    </div>
  );
}
