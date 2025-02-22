import React, {useState, useContext, useEffect} from 'react';
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
import { ArticleContext } from '../../contexts/article_context';

const HomePage = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const {username, user_id, interested_in} = useContext(UserContext)
    const [search, set_search] = useState("");
    const [stocks, set_stocks] = useState([]);
    const {getSuggestions, set_selected_stocks, selected_stocks} = useContext(StocksContext)
    const {articles, getArticles} = useContext(ArticleContext)
    useEffect(() => {
        getSuggestions(search, set_stocks)
    }, [search]);
    useEffect(()=>{
        getArticles()
    },[])
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
                                <span className={styles['stock-ticker']} key={index}>{item.ticker} </span> <span>|</span> <span className={styles['stock-name']}>{item.stock_name}</span>
                            </div>
                        ))
                    }
                </div>
                <div className={styles['logout-container']}>
                    <Link className={styles['logout-btn']}><img src={LogoutIcon} alt="Logout icon"/> Logout</Link>
                </div>
            </div>
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
                        
                        articles.map((article)=>( 
                            <div className={styles['article-card']}>
                                <div className={styles['stock-info']}>
                                    <p className={styles['stock-short-name']}>
                                       {article.stock_ticker}
                                    </p>
                                    <p className={styles['stock-full-name']}>
                                        Artificial And Big Type Script
                                    </p>
                                    <p className={styles['stock-price']}>
                                        115.5$
                                    </p>
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
                                            George Washington
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
                        <div className={styles['stock-article-text']}>
                            <p>
                                In a report released today, from William Blair maintained a Hold rating on Re/Max
                                Holdings (
                                – ). The company’s shares closed today at $9.11. According to , Sheldon is a 3-star
                                analyst
                                with an average return of and a 47.37% success rate. Re/Max Holdings has an analyst
                                consensus of Moderate Sell, with a price target consensus of $7.50.
                                RMAX market cap is currently $319M and has a P/E ratio of -18.99. Based on the recent
                                corporate insider activity of 67 insiders, corporate insider sentiment is positive on
                                the
                                stock. This means that over the past quarter there has been an increase of insiders
                                buying
                                their shares of RMAX in relation to earlier this year. Last month, Adam K Peterson, a
                                Major
                                Shareholder at RMAX bought 11,798.00 shares for a total of $113,732.72.
                                I find myself hard-pressed, at times, to believe how often legacy automaker Ford can
                                issue
                                recalls on its products. In fact, another one just showed up, this time covering nearly
                                a
                                quarter of a million vehicles. And even investors look like they have had it with Ford;
                                shares are down nearly 1.5% in Friday afternoon’s trading. This time, the recall targets
                                Lincoln Aviators and Ford Explorers made between 2020 and 2021, the worst parts of the
                                pandemic. That encompasses 240,510 such vehicles, and the focus is on seat belt anchor
                                bolts. More specifically, the bolts may be improperly secured, which means that, in some
                                cases, the whole housing could come undone, and that might be one of the last things
                                anyone
                                would want to see in a wreck. The fix is rather simple; once again, Ford owners will
                                need to
                                return to their dealership of choice, where dealers will inspect the bolts. Should they
                                be
                                found to be part of the problem, the bolts and related components will be replaced.
                                There
                                will likely be no charge for this, except for the time you lose for them.
                                And good news for anyone paralyzed with indecision over the sheer cost of a car these
                                days;
                                the Ford Bronco’s new discount packages are still in play, and will continue to be so
                                for
                                the near term future, if nothing else. The 2024 Ford Bronco sport can still be had with
                                a
                                discount of $2,750 off, as well as “low-interest financing.” Plus, there are lease deals
                                involved for anyone who would rather go that route. There is $2,000 in “conquest cash”
                                still
                                available for those who owned or leased a Jeep, as well as for those who owned or leased
                                a
                                General Motors vehicle. Neither trade-ins nor lease terminations are required, either.
                                However, the 2025 Ford Bronco Sport does not have any incentives on it. At least, not
                                yet;
                                that could change the farther into the new market year we get. Turning to Wall Street,
                                analysts have a Hold consensus rating on F stock based on four Buys, eight Holds and
                                three
                                Sells assigned in the past three months, as indicated by the graphic below. After a
                                17.81%
                                over the past year, the of $10.56 per share implies 13.98% upside potential.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default HomePage;