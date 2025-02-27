import { createContext, useState, useContext, useEffect } from "react";
import toast from "react-hot-toast";
import {useQuery} from "@tanstack/react-query"
import { get, put, _delete, post } from "../api/api";
import { UserContext } from "./user_context";
import { data } from "react-router";

export const ArticleContext = createContext(); 

const ArticleContextProvider = ({ children }) => {
    const [articles, set_articles] = useState([]);
    const [stock_data, set_stock_data] = useState([])

    // Use useEffect to log the updated articles state
    useEffect(() => {
        console.log("Articles updated:", articles);
    }, [articles]); // This effect runs whenever `articles` changes


 


    const getArticles = async () => {
        const res = await get(`processed_articles`);
        if (res.data) {
            let filtered_list = res.data.Items.filter((item)=> item.stock_ticker !== "Unkown")
            set_articles(filtered_list ); // State update is scheduled
        } else {
            toast.error("Could not get articles");
        }
    };

    const getStockData= async (stock_name)=>{
        const res = await get(`get_ticker_data/?ticker=${stock_name}`)
        if (res.data){
            set_stock_data(res.data.Items); 
        }
        else{
            toast.error("could not get stock data"); 
        }
    }

    

    return (
        <ArticleContext.Provider
            value={{
                getArticles,
                articles,
                getStockData, 
                stock_data
            }}
        >
            {children}
        </ArticleContext.Provider>
    );
};

export default ArticleContextProvider;