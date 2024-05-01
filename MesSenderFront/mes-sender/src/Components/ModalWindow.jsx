import { PushButton } from "./Buttons";
import styles from "./Styles/ModalWindow.module.css";
import classnames from "classnames";

export default function ModalWindow({ modalState, setModalState, style }) {
  function close() {
    setModalState({ isOpen: false });
  }
  return (
    <div
      className={styles.modalWindow}
      style={{ display: modalState.isOpen ? "block" : "none" }}
    >
      <div className={styles.modalContentContainer}>
        <div className={classnames(styles.modalContent, style)}>
          <p className={styles.textStyle}>
            {modalState.isOpen && modalState.text}
          </p>
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
