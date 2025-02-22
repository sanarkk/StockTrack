import React, {useContext, useEffect, useState} from "react";
import styles from "./ChooseStocksModal.module.scss";
import SearchIcon from "../../../assets/icons/searchIcon.png";
import {StocksContext} from "../../../contexts/stocks_context";
import SearchBar from "../../SearchBar/SearchBar";
import StockList from "../StockList/StockList";
import {UserContext} from "../../../contexts/user_context";
import { XMarkIcon } from "@heroicons/react/24/solid";
const ChooseStocksModal = ({setIsModalOpen}) => {
    const {
        getSuggestions,
        stock_suggestions_status,
        stock_lists,
        selected_stocks,
        set_selected_stocks,
        saveSelectedStocks,
    } = useContext(StocksContext);
    const {interested_in} = useContext(UserContext);
    const [search_state, set_search_state] = useState("");
    const [suggestions, set_suggestions] = useState([])


    useEffect(() => {
        getSuggestions(search_state, set_suggestions);
    }, [search_state]);

    const handleSelectStock = (word) => {
        if (!selected_stocks.includes(word)) {
            set_selected_stocks([...selected_stocks, word]);
        } else {
            set_selected_stocks(selected_stocks.filter((w) => w !== word));
        }
    };


    return (
        <div className={styles.overlay}>
            <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
                <div className={styles['stocks-container']}>
                    <SearchBar search_state={search_state} set_search_state={set_search_state}/>
                    <StockList stocks={suggestions} selected_stocks={selected_stocks}
                               handleSelectStock={handleSelectStock} interested_in={interested_in}/>
                </div>
                <div className={styles['buttons']}>
                    <div className={styles['continue-btn-container']}>
                        <button className={styles.closeBtn} onClick={() => {
                            saveSelectedStocks();
                            setIsModalOpen(false)
                        }}>Update Stocks
                        </button>
                    </div>
                    <div className={styles["close-btn-container"]}>
                        <button onClick={() => setIsModalOpen(false)} className={styles['close-btn']}>
                            Close
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChooseStocksModal;
