import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import LoginPage from "./components/LoginPage/LoginPage";
import UserContextProvider from "./contexts/user_context.jsx";
import StocksContextProvider from "./contexts/stocks_context.jsx";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import HomePage from "./components/HomePage/HomePage.jsx";
import ArticleContextProvider from "./contexts/article_context.jsx";
import { QueryClientProvider, QueryClient } from "react-query";

const root = ReactDOM.createRoot(document.getElementById("root"));
const queryClient = new QueryClient();
root.render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
     <BrowserRouter> {/* ✅ Wrap everything inside BrowserRouter */}
     
    <UserContextProvider>
        <StocksContextProvider>
          <ArticleContextProvider>
          
        <Routes>
          <Route path="/" element={<LoginPage />} />
          <Route path="/home" element={<HomePage />} />
        </Routes>

      <Toaster />
      </ArticleContextProvider>
      </StocksContextProvider>
    </UserContextProvider>
   
    </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>
);