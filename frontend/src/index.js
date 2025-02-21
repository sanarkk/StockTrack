<<<<<<< HEAD
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import {createBrowserRouter, RouterProvider} from 'react-router-dom';
import LoginPage from "./components/LoginPage/LoginPage";
import HomePage from "./components/HomePage/HomePage";

const router = createBrowserRouter([{
    path: '/',
    element: <LoginPage/>,
}, {
    path: '/home',
    element: <HomePage/>,
}]);

const root = ReactDOM.createRoot(document.getElementById('root'));
=======
import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import LoginPage from "./components/LoginPage/LoginPage";
import UserContextProvider from "./contexts/user_context.jsx";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

const router = createBrowserRouter([
  {
    path: "/",
    element: <LoginPage />,
  },
  {
    path: "/home",
    element: <LoginPage />,
  },
]);

const root = ReactDOM.createRoot(document.getElementById("root"));
>>>>>>> f0d6aed (added context)
root.render(
  <React.StrictMode>
    <UserContextProvider> 
      <RouterProvider router={router} />
    </UserContextProvider>
  </React.StrictMode>
);
