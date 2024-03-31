import styles from "./TextField.module.css";

export function TextFieldBase({ style, placeholder = "" }) {
  return (
    <input
      style={style}
      className={styles.textFieldBase}
      placeholder={placeholder}
    ></input>
  );
}
