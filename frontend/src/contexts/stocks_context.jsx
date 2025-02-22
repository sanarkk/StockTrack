import { get,put,_delete, post } from "../api/api";
import { createContext, useState } from "react";
import { useNavigate } from "react-router";
import toast from "react-hot-toast";


export const StocksContext = createContext(); 
const StocksContextProvider = ({children})=>{
    const [stocks_list, set_stock_list] = useState([])
    const [stock_suggestions, set_stock_suggestions] = useState([]); 
    const [stock_suggestions_status, set_stock_suggestions_status] = useState(false)
    const [selected_stocks, set_selected_stocks] = useState([])
    
    const getSuggestions = async (searchInput)=>{
        const res = await post(`search?data=${searchInput}`); 
        if(res.data){
            set_stock_suggestions(res.data.Items); 
        }
        else if (res.status_code != 1){
            set_stock_suggestions_status(false); 
        }
        else{
            toast.error("could not get stock suggestions"); 
            set_stock_suggestions_status(false); 
        }
    }

    const getStocks = (payload)=>{


    }





    return(
        <StocksContext.Provider
            value={{
                stocks_list, stock_suggestions, stock_suggestions_status, getSuggestions, set_stock_suggestions, selected_stocks, set_selected_stocks       
            }}
        >
            {children}
        </StocksContext.Provider>
    )

}


export default StocksContextProvider