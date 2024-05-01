import { createContext, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import ModalWindow from "./ModalWindow";
export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [modalState, setModalState] = useState({ isOpen: false });

  const showModal = useCallback((text) => {
    setModalState({ isOpen: true, text: text });
  }, []);

  const getCurrentUser = useCallback(async () => {
    try {
      const response = await fetch(`/api/users/me`);
      switch (response.status) {
        case 401:
        case 403:
          navigate("/login");
          break;
        case 200:
          setUser(await response.json());
          break;
        default:
          throw Error(
            "Ошибка при обращении к серверу.Статус ответа: " + response.status
          );
      }
    } catch (err) {
      console.log(err);
      showModal("Произошла ошибка при обращении к серверу");
    }
  }, [navigate, showModal]);

  const logout = useCallback(async () => {
    try {
      const response = await fetch(`/api/auth/logout`, {
        method: "POST",
      });
      switch (response.status) {
        case 204:
          setUser(null);
          navigate("/login");
          break;
        default:
          throw Error(
            "Ошибка при обращении к серверу.Статус ответа: " + response.status
          );
      }
    } catch (err) {
      console.log(err);
      showModal("Произошла ошибка при обращении к серверу");
    }
  }, [navigate, showModal]);

  const contextValue = {
    user,
    setUser,
    getCurrentUser,
    logout,
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
