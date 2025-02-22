import React, { useState, useEffect, useContext } from "react";
import styles from "./SearchBar.module.scss";
import { StocksContext } from "../../contexts/stocks_context";

const SearchBar = () => {
    const [searchInput, setSearchInput] = useState("");
    const {getSuggestions, stock_suggestions_status, stock_suggestions, stock_lists, set_stock_suggestions, selected_stocks, set_selected_stocks} = useContext(StocksContext); 

    useEffect(() => {
        console.log("eee")
        getSuggestions(searchInput); 
    }, [searchInput]);

    const handleSelectStock = (word) => {
        set_selected_stocks([...selected_stocks, word]);
        setSearchInput(""); // Optionally clear search input after selecting
        set_stock_suggestions([]); // Clear suggestions after selection
    };

    const handleRemoveStock = (word) => {
        set_selected_stocks(selected_stocks.filter((w) => w !== word));
    };

    return (
        <div className={styles.searchContainer}>
            <input
                type="text"
                placeholder="Search by stock..."
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
                className={styles.searchInput}
            />

            {searchInput && (
                <ul className={styles.suggestionsList}>
                    {stock_suggestions.map((word, index) => (
                        <li
                            key={index}
                            className={styles.suggestionItem}
                            onClick={() => handleSelectStock(word)}
                        >
                            {word.username}
                        </li>
                    ))}
                </ul>
            )}

            <div className={styles.selectedWords}>
                {selected_stocks.map((word, index) => (
                    <div key={index} className={styles.selectedWord}>
                        <span>{word.username}</span>
                        <button onClick={() => handleRemoveStock(word)} className={styles.removeBtn}>Remove Stock</button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SearchBar;
