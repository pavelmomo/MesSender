import styles from "./Buttons.module.css";
import classNames from "classnames";

export function ButtonWithIcon({ icon, style, text }) {
  return (
    <button
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
    </button>
  );
}

export function IconButton({ icon, style }) {
  return (
    <div style={style} className={classNames(styles.button, styles.buttonIcon)}>
      {icon}
    </div>
  );
}
export function PushButton({ style, text, onClick }) {
  return (
    <button
      style={style}
      onClick={onClick}
      className={classNames(styles.button, styles.pushButton)}
    >
      <p>{text}</p>
    </button>
  );
}
