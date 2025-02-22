import React from "react";
import styles from "./ChooseStocksModal.module.scss";
import SearchIcon from "../../../assets/icons/searchIcon.png";

const ChooseStocksModal = ({isOpen, onClose}) => {
    
    if (!isOpen) return null;

    const requestForStock = (e) => {
        //Make request to backend every time when user types in new character
    }

    return (
        <div className={styles.overlay}>
            <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
                <div className={styles['stocks-container']}>
                    <div className={styles['sort-by-stock-container']}>
                        <img src={SearchIcon} alt=""/>
                        <input onChange={(e) => requestForStock(e)} type="text" placeholder="Search for stock..."
                               className={styles['sort-by-stock-input']}/>
                    </div>
                </div>
                <div className={styles['continue-btn-container']}>
                    <button className={styles.closeBtn} onClick={onClose}>Continue</button>
                </div>
            </div>
        </div>
    );
};

export default ChooseStocksModal;
