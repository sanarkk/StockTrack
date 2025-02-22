import { get,put,_delete, post } from "../api/api";
import { createContext, useState, useContext } from "react";
import { useNavigate } from "react-router";
import toast from "react-hot-toast";
import { UserContext } from "./user_context";

export const StocksContext = createContext(); 
const StocksContextProvider = ({children})=>{
    const [stocks_list, set_stock_list] = useState([])
    const [stock_suggestions_status, set_stock_suggestions_status] = useState(false)
    const [selected_stocks, set_selected_stocks] = useState([])

    const {username, interested_in, refresh_user} = useContext(UserContext)
    
    const getSuggestions = async (searchInput,set_suggestions)=>{
        const res = await post(`search?data=${searchInput}`); 
        if(res.data){
            set_suggestions(res.data.Items);
        }
        else{
            toast.error("could not get stock suggestions"); 
            set_stock_suggestions_status(false); 
        }
    }

    const saveSelectedStocks = async ()=>{
        const res = await post(`stock_preferences?username=${username}`, selected_stocks)
        if(res.status_code == 200){
            refresh_user();
            toast.success("stocks saved to preferences")
        }
        else{
            toast.error("could not save stocks")
        }
    }

    
    const getUserStocks = async ()=>{ 
        const res = await get(`get_tickers/?username=${username}`)
        if(res.data){
            set_stock_list(res.data.interested_in.Items)
        }
        else{
            toast.error("could not save stocks")
        }
    }

    // const updateSelectedStocks = async(stock_list, operation)=>{
    //     let new_stock_list;
    //     const user_stock_list = interested_in.map((stock) => stock.ticker);
    //     if(operation == "add"){
    //         new_stock_list = [...stock_list,...user_stock_list];
    //     }
    //     else{
    //         new_stock_list = user_stock_list.filter((stock) => !stock_list.includes(stock));
    //     }
    //     const res = await post(`stock_preferences?username=${username}`, new_stock_list);
    //     if(res.status_code == 200){
    //         refresh_user();
    //         toast.success("stock list updated");
    //     }
    //     else{
    //         toast.error("could not update stock list");
    //     }
    // }





    return(
        <StocksContext.Provider
            value={{
                stocks_list,  stock_suggestions_status, getSuggestions,  selected_stocks, set_selected_stocks, saveSelectedStocks,
            }}
        >
            {children}
        </StocksContext.Provider>
    )

}


export default StocksContextProvider