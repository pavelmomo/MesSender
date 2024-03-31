import React, { useState } from "react";
import UserView from "./Views/UserView";
import "./index.css";

export default function App() {
  const [user, setUser] = useState({ id: 1 });
  return (
    <>
      <UserView user />
    </>
  );
}
