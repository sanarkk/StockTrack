import React, { useState, useEffect, useContext } from "react";
import styles from "./SearchBar.module.scss";
import { StocksContext } from "../../contexts/stocks_context";
import StockList from "../HomePage/StockList/StockList";


const SearchBar = (props) => {



    return (
        <div className={styles['sort-by-stock-container']}>
            <input
                type="text"
                placeholder="Search by stock..."
                value={props.search_state}
                onChange={(e) => props.set_search_state(e.target.value)}
                className={styles['sort-by-stock-input']}
            />
        </div>
    );
};

export default SearchBar;
