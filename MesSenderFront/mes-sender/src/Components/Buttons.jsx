import { NavLink } from "react-router-dom";
import styles from "./Styles/Buttons.module.css";
import classNames from "classnames";

export function ButtonWithIcon({ icon, style, text, linkPath, onClick }) {
  return (
    <NavLink
      to={linkPath}
      onClick={onClick}
      style={style}
      className={classNames(styles.button, styles.buttonList)}
    >
      <div style={{ margin: 5, marginLeft: 12, marginRight: 16 }}>{icon}</div>
      <h6
        style={{
          flex: 1,
          margin: 3,
          alignContent: "center",
          textAlign: "left",
        }}
      >
        {text}
      </h6>
    </NavLink>
  );
}

export function IconButton({ icon, style, onClick }) {
  return (
    <button
      onClick={onClick}
      style={style}
      className={classNames(styles.button, styles.buttonIcon)}
    >
      {icon}
    </button>
  );
}
export function PushButton({
  style,
  text,
  onClick,
  type,
  className,
  onSubmit,
  isDisabled,
}) {
  return (
    <button
      disabled={isDisabled ? "disabled" : ""}
      onSubmit={onSubmit}
      type={type}
      style={style}
      onClick={onClick}
      className={classNames(styles.button, styles.pushButton, className)}
    >
      <p>{text}</p>
    </button>
  );
}
