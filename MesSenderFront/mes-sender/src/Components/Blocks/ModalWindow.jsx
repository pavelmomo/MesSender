import { useContext } from "react";
import { PushButton } from "../Buttons";
import styles from "../Styles/ModalWindow.module.css";
import classnames from "classnames";
import { AuthContext } from "../AuthProvider";

export default function ModalWindow({ style, text }) {
  const { isModalOpen, setModalOpen } = useContext(AuthContext);

  function close() {
    setModalOpen(false);
  }

  return (
    <div
      className={styles.modalWindow}
      style={{ display: isModalOpen ? "block" : "none" }}
    >
      <div className={styles.modalContentContainer}>
        <div className={classnames(styles.modalContent, style)}>
          <p className={styles.textStyle}>{text}</p>
          <PushButton
            onClick={close}
            text="Ок"
            className={styles.buttonStyle}
          ></PushButton>
        </div>
      </div>
    </div>
  );
}
