import { createContext, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import ModalWindow from "./Blocks/ModalWindow";
export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [modalState, setModalState] = useState({ isOpen: false });

  const getCurrentUser = useCallback(async () => {
    const response = await fetch(`/api/users/me`);
    switch (response.status) {
      case 401:
        navigate("/login");
        break;
      case 200:
        setUser(await response.json());
        break;
      default:
        break;
    }
  }, []);

  const logout = useCallback(async () => {
    const response = await fetch(`/api/auth/logout`, {
      method: "POST",
    });
    switch (response.status) {
      case 204:
        setUser(null);
        navigate("/login");
        break;
      default:
        break;
    }
  }, []);

  const login = useCallback(async (e) => {
    const response = await fetch(`/api/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        username: e.target.username.value,
        password: e.target.password.value,
      }),
    });
    return response.status;
  }, []);
  const register = useCallback(async (e) => {
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
    return response.status;
  }, []);
  const showModal = useCallback((text) => {
    setModalState({ isOpen: true, text: text });
  }, []);

  const contextValue = {
    user,
    setUser,
    getCurrentUser,
    logout,
    login,
    register,
    showModal,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
      <ModalWindow
        modalState={modalState}
        setModalState={setModalState}
      ></ModalWindow>
    </AuthContext.Provider>
  );
};
