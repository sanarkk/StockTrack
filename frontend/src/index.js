import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import LoginPage from "./components/LoginPage/LoginPage";

import {createBrowserRouter, RouterProvider} from 'react-router-dom';

const router = createBrowserRouter([{
    path: '/',
    element: <LoginPage/>,
}]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <RouterProvider router={router}/>
    </React.StrictMode>
);
