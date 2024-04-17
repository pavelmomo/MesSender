import React, { useState, useEffect } from "react";
import { Routes, Route, Navigate, BrowserRouter } from "react-router-dom";
import MainLayout from "./Components/Pages/MainLayout";
import "./index.css";
import DialogsTab from "./Components/Tabs/DialogsTab";
import UsersTab from "./Components/Tabs/UsersTab";
import { AuthProvider } from "./Components/AuthProvider";
import Login from "./Components/Pages/Login";
import Register from "./Components/Pages/Register";
import ProfileTab from "./Components/Tabs/ProfileTab";

const url = "localhost:8000";

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<MainLayout />}>
            <Route index element={<Navigate to="dialogs" />} />
            <Route path="dialogs" element={<DialogsTab />} />
            <Route path="users" element={<UsersTab />} />
            <Route path="profile" element={<ProfileTab />} />
          </Route>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/logout" element={<UsersTab />} />
          <Route path="*" element={<h2> 404: Страница не найдена </h2>} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export { url };
