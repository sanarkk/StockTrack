import React, {useState, useContext} from 'react';
import styles from "./HomePage.module.scss"
import {Link} from "react-router";
import LogoutIcon from '../../assets/icons/logoutIcon.png'
import SearchIcon from '../../assets/icons/searchIcon.png'
import SortByDateDropdown from "./SortByDateDropdown/SortByDateDropdown";
import ChooseStocksModal from "./ChooseStocksModal/ChooseStocksModal";
import { UserContext } from '../../contexts/user_context';
import SearchBar from '../SearchBar/SearchBar';

const HomePage = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const {username, user_id,interested_in} = useContext(UserContext)
    return (
        <div className={styles.wrapper}>
            <div className={styles.sidebar}>
                <div className={styles['logo-container']}>
                    <p className={styles.logo}>StockTrack</p>
                </div>
                <div className={styles['stocks-container']}>

                </div>
                <div className={styles['logout-container']}>
                    <Link className={styles['logout-btn']}><img src={LogoutIcon} alt="Logout icon"/> Logout</Link>
                </div>
            </div>
            <div className={styles['main-container']}>
                <div className={styles.header}>
                    <div className={styles['sort-container']}>
                        <SortByDateDropdown/>
                       <SearchBar/>
                    </div>
                    <p className={styles.username}>Welcome back, <span>{username}</span></p>
                </div>
                <div className={styles['articles-container']}>
                    <button onClick={() => setIsModalOpen(true)}>Open Modal</button>
                    <ChooseStocksModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}/>
                </div>
            </div>
        </div>
    )
}

export default HomePage;