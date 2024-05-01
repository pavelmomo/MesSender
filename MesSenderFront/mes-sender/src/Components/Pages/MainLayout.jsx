import { Outlet } from "react-router-dom";
import Menu from "../Menu";
import { useEffect, useContext } from "react";
import { AuthContext } from "../AuthProvider";

const mainContainerStyle = {
  display: "flex",
  flexDirection: "row",
  height: "100vh",
};

export default function MainLayout() {
  const { user, getCurrentUser } = useContext(AuthContext);
  useEffect(() => {
    getCurrentUser();
  }, []);

  if (user == null) return;

  return (
    <main>
      <div style={mainContainerStyle}>
        <Menu />
        <Outlet />
      </div>
    </main>
  );
}
