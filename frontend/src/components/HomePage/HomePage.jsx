import React, {useState, useContext, useEffect, useRef} from 'react';
import styles from "./HomePage.module.scss"
import {Link} from "react-router";
import LogoutIcon from '../../assets/icons/logoutIcon.png'
import SearchIcon from '../../assets/icons/searchIcon.png'
import SortByDateDropdown from "./SortByDateDropdown/SortByDateDropdown";
import ChooseStocksModal from "./ChooseStocksModal/ChooseStocksModal";
import {UserContext} from '../../contexts/user_context';
import SearchBar from '../SearchBar/SearchBar';
import StockList from "./StockList/StockList";
import {StocksContext} from "../../contexts/stocks_context";
import SecondStockList from "./SecondStockList/SecondStockList";
import Logo from "../../assets/logo.png"
import AddIcon from "../../assets/icons/add.png"
import {ArticleContext} from '../../contexts/article_context';
import green_arrow from "./svgs/up.svg"
import red_arrow from "./svgs/down.svg"
import LineChart from "./LineChart";
import { useQuery } from '@tanstack/react-query';
import { QRCodeCanvas } from "qrcode.react";

const HomePage = () => {
    const {username, user_id, interested_in, logout} = useContext(UserContext)
    const [isModalOpen, setIsModalOpen] = useState(interested_in.length === 0?true:false);
    const [search, set_search] = useState("");
    const [stocks, set_stocks] = useState([]);
    const {getSuggestions, set_selected_stocks, selected_stocks} = useContext(StocksContext)
    const {articles, getArticles, getStockData, stock_data} = useContext(ArticleContext)
    const [display_article, set_display_article] = useState(articles[0])
    const [qrCodeOpened, set_qrCodeOpened] = useState(false)

    const [TelegramLinkForChatBot, setTelegramLinkForChatBot] = useState("t.me/StockTrackNotifications_bot");

    useEffect(() => {
        getSuggestions(search, set_stocks)
    }, [search]);
    useEffect(() => {
        getArticles()
    }, [])

    useEffect(() => {
        set_display_article(articles[0])
    }, [articles])
    useEffect(() => {
        if (display_article) {
            getStockData(display_article.stock_ticker);
            console.log(stock_data)
        }
    }, [display_article])
    useEffect(() => {
        console.log(stock_data)
    }, [stock_data])

    useQuery({
        queryKey: ["articles"], // Unique key for caching
        queryFn: getArticles
     
      });

    return (
        <div className={styles.wrapper}>
            <div className={styles.sidebar}>
                <div className={styles['logo-container']}>
                    <img draggable="false" className={styles.logo} src={Logo} alt=""/>
                </div>
                <div className={styles['stocks-editor-container']}>
                    <p className={styles['your-stocks']}>Your stocks:</p>
                    <button onClick={() => {
                        set_selected_stocks(interested_in.map((stock) => stock.ticker));
                        setIsModalOpen(true)
                    }} className={styles['add-more-stocks-btn']}>Edit Stocks
                        <img src={AddIcon} alt=""/>
                    </button>
                </div>
                {
                    isModalOpen &&
                    <ChooseStocksModal setIsModalOpen={setIsModalOpen}/>
                }
                <div className={styles['stocks-container']}>
                    {
                        interested_in.map((item, index) => (
                            <div className={styles.stock}>
                                <span className={styles['stock-ticker']} key={index}>{item.ticker} </span>
                                <span>|</span> <span className={styles['stock-name']}>{item.stock_name}</span>
                            </div>
                        ))
                    }
                </div>
                <div className={styles["logout-container"]}>
                    <button onClick={() => logout()} className={styles["logout-btn"]}>
                        <img src={LogoutIcon} alt="Logout icon"/> Logout
                    </button>
                    <button onClick={() => set_qrCodeOpened(!qrCodeOpened)} className={styles["logout-btn"]}>
                        Open QR-Code
                    </button>
                </div>
            </div>
            {qrCodeOpened && (
                <div className={styles["qrcode-container"]}>
                    <div className={styles.modal}>
                        {TelegramLinkForChatBot && <QRCodeCanvas value={TelegramLinkForChatBot} size={500}/>}
                        <br/>
                        <button className={styles['close-qrcode-btn']} onClick={() => set_qrCodeOpened(false)}>Close</button>
                    </div>
                </div>
            )}
            <div className={styles['main-container']}>
                <div className={styles.header}>
                    <div className={styles['sort-container']}>
                    <SortByDateDropdown/>
                        <SearchBar search_state={search} set_search_state={set_search}/>
                    </div>
                    <p className={styles.username}>Welcome back, <span>{username}</span></p>
                </div>
                <div className={styles['articles-container']}>
                    {/*<button onClick={() => setIsModalOpen(true)}>Open Modal</button>*/}
                    {/*<ChooseStocksModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}/>*/}
                    <div className={styles['articles-card-container']}>
                        {

                            articles.map((article) => (
                                <div onClick={() => {
                                    set_display_article(article)
                                }} className={styles['article-card']}>
                                    <div className={styles['stock-info']}>
                                        <p className={styles['stock-short-name']}>
                                            {article.stock_ticker}
                                        </p>
                                        <p className={styles['stock-full-name']}>
                                           Sentiment score:  {Math.round(article.sentiment_score * 100) / 100}
                                        </p>
                                        <img style={{width: "35px", height: "35px"}}
                                             src={article.sentiment == "POSITIVE" ? green_arrow : red_arrow} alt=""/>
                                    </div>
                                    <div className={styles.bar}/>
                                    <div className={styles['article-info']}>
                                        <p className={styles['article-title']}>
                                            {article.title}
                                        </p>
                                        <p className={styles['stock-short-description']}>
                                            {article.summary}
                                        </p>
                                        <div className={styles['stock-details']}>
                                            <p className={styles.author}>
                                                {article.news_source}
                                            </p>
                                            <p className={styles['stock-date']}>
                                                {article.publish_date}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            ))

                        }
                    </div>
                    <div className={styles['stock-article']}>
                        {
                            stock_data && (<LineChart/>)
                        }


                        <div className={styles['stock-article-text']}>
                            <p>
                                {display_article ? display_article.article_text : ""}
                            </p>
                            
                        </div>
                        <div className={styles['article-btn-container']}>
                            {display_article&&
                       <    Link className={styles['check-article-button']} target='_blank' to={display_article.url}>See full article</Link>
                            }
                        </div>
                        
                    </div>
                </div>
            </div>
        </div>
    )
}

export default HomePage;