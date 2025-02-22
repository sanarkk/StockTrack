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
  console.log(stock_data)
  const dates = stock_data.map((item) => {return item.date})
  const prices = stock_data.map((item) => {return item.open})


  const data = {
    labels: dates,
    datasets: [
      {
        label: "Ticker Price",
        data: prices,
        fill: false,
        borderColor: "rgb(255, 0, 0)",
        tension: 0.1,
      },
    ],
  };
  return <Line data={data} options={options} />;
};

export default LineChart;