import { createContext, useState, useContext, useEffect } from "react";
import toast from "react-hot-toast";
import { get, put, _delete, post } from "../api/api";
import { UserContext } from "./user_context";

export const ArticleContext = createContext(); 

const ArticleContextProvider = ({ children }) => {
    const [articles, set_articles] = useState([]);

    // Use useEffect to log the updated articles state
    useEffect(() => {
        console.log("Articles updated:", articles);
    }, [articles]); // This effect runs whenever `articles` changes

    const getArticles = async () => {
        const res = await get(`processed_articles`);
        if (res.data) {
            set_articles(res.data.Items); // State update is scheduled
        } else {
            toast.error("Could not get articles");
        }
    };

    return (
        <ArticleContext.Provider
            value={{
                getArticles,
                articles,
            }}
        >
            {children}
        </ArticleContext.Provider>
    );
};

export default ArticleContextProvider;