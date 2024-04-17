import { createContext, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [isModalOpen, setModalOpen] = useState(false);

  const getCurrentUser = useCallback(async () => {
    const response = await fetch(`/api/users/current`);
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
  }, [navigate]);

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
  }, [navigate]);

  const contextValue = {
    user,
    setUser,
    isModalOpen,
    setModalOpen,
    getCurrentUser,
    logout,
  };

  return (
    <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
  );
};
