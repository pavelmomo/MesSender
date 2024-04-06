import styles from "../Styles/TextField.module.css";
import classNames from "classnames";

export function TextFieldBase({
  style,
  type,
  placeholder = "",
  className,
  name,
}) {
  return (
    <input
      name={name}
      type={type}
      style={style}
      className={classNames(styles.textFieldBase, className)}
      placeholder={placeholder}
    ></input>
  );
}
