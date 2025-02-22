import React, { useState, useEffect, useContext } from "react";
import styles from "./SearchBar.module.scss";
import { StocksContext } from "../../contexts/stocks_context";

const SearchBar = () => {
    const [searchInput, setSearchInput] = useState("");
    const {getSuggestions, stock_suggestions_status, stock_suggestions, stock_lists, set_stock_suggestions} = useContext(StocksContext); 
    const [selectedWords, setSelectedWords] = useState([]);

    useEffect(() => {
        getSuggestions(searchInput); 
        // if (searchInput.length > 0) {
        //     // Make request to backend as the user types
        //     const fetchSuggestions = async () => {
        //         try {
        //             const response = await axios.get(`/api/words?query=${searchInput}`);
        //             setSuggestions(response.data); // Assuming backend returns an array of words
        //         } catch (error) {
        //             console.error("Error fetching suggestions:", error);
        //         }
        //     };

        //     fetchSuggestions();
        // } else {
        //     setSuggestions([]); // Clear suggestions if input is empty
        // }
    }, [searchInput]);

    const handleSelectWord = (word) => {
        setSelectedWords((prevWords) => [...prevWords, word]);
        setSearchInput(""); // Optionally clear search input after selecting
        set_stock_suggestions([]); // Clear suggestions after selection
    };

    const handleRemoveWord = (word) => {
        setSelectedWords((prevWords) => prevWords.filter((w) => w !== word));
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
                    {suggestions.map((word, index) => (
                        <li
                            key={index}
                            className={styles.suggestionItem}
                            onClick={() => handleSelectWord(word)}
                        >
                            {word}
                        </li>
                    ))}
                </ul>
            )}

            <div className={styles.selectedWords}>
                {selectedWords.map((word, index) => (
                    <div key={index} className={styles.selectedWord}>
                        <span>{word}</span>
                        <button onClick={() => handleRemoveWord(word)} className={styles.removeBtn}>×</button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SearchBar;
