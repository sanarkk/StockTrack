import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import LoginPage from "./components/LoginPage/LoginPage";
import UserContextProvider from "./contexts/user_context.jsx";
import StocksContextProvider from "./contexts/stocks_context.jsx";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import HomePage from "./components/HomePage/HomePage.jsx";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
     <BrowserRouter> {/* ✅ Wrap everything inside BrowserRouter */}
    <UserContextProvider>
        <StocksContextProvider>
     
        <Routes>
          <Route path="/" element={<LoginPage />} />
          <Route path="/home" element={<HomePage />} />
        </Routes>
     
      <Toaster />
      </StocksContextProvider>
    </UserContextProvider>
    </BrowserRouter>
  </React.StrictMode>
);