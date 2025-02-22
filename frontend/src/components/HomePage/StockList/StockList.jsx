import React from 'react';
import styles from './StockList.module.scss';

const StockList = ({handleSelectStock,selected_stocks, stocks,interested_in}) => {
    return (
        <div className={styles['stock-list']}>
            {stocks.map((stock) => (
                <div
                    key={stock.stock_name}
                    className={selected_stocks.includes(stock.ticker)? styles['selected-stock-list-item'] : styles['stock-list-item']}
                    onClick={() => handleSelectStock(stock.ticker)}
                >
                    <button className={selected_stocks.includes(stock.ticker)? styles['selected-stock-list-item-btn'] : styles['stock-list-item-btn']}>{stock.stock_name}</button>
                </div>
            ))}
        </div>
    )
}

export default StockList;