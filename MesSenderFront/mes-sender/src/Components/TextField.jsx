import styles from "./Styles/TextField.module.css";
import classNames from "classnames";

export function TextFieldBase({
  style,
  type,
  placeholder = "",
  className,
  name,
  defaultValue,
  isDisabled,
  onChange,
  value,
}) {
  return (
    <input
      maxLength="490"
      disabled={isDisabled ? "disabled" : ""}
      onChange={onChange}
      value={value}
      defaultValue={defaultValue}
      autoComplete="off"
      name={name}
      type={type}
      style={style}
      className={classNames(styles.textFieldBase, className)}
      placeholder={placeholder}
    ></input>
  );
}
