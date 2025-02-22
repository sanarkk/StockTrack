import React from "react";
import { Line } from "react-chartjs-2";
import {ArticleContext} from "../../contexts/article_context";
import {useContext} from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

// Register required chart.js components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);



const options = {
  responsive: true,
  plugins: {
    legend: {
      display: true,
      position: "top",
    },
    title: {
      display: true,
      text: "Stock Prices Over the Week",
    },
  },
  scales: {
    x: {
      title: {
        display: true,
        text: "Days of the Week",
      },
    },
    y: {
      title: {
        display: true,
        text: "Price (USD)",
      },
    },
  },
};

const LineChart = () => {
  const {stock_data} = useContext(ArticleContext)
  const dates = stock_data.map((item) => {return item.date})
  const low_prices = stock_data.map((item) => {return item.low})
  const high_prices = stock_data.map((item) => {return item.high})
  


  const data = {
    labels: dates,
    datasets: [
      {
        label: "Low Price",
        data: low_prices,
        fill: false,
        borderColor: "rgb(255, 0, 0)",
        tension: 0.1,
      },
      {
        label: "High Price",
        data: high_prices,
        fill: false,
        borderColor: "rgb(0, 255, 0)",
        tension: 0.1,
      },
 
    ],
  };
  return <Line data={data} options={options} />;
};

export default LineChart;