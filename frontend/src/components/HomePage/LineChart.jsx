import React from "react";
import { Line } from "react-chartjs-2";
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

const labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

const data = {
  labels: labels,
  datasets: [
    {
      label: "Ticker Price",
      data: [65, 59, 80, 81, 56, 55, 40],
      fill: false,
      borderColor: "rgb(255, 0, 0)",
      tension: 0.1,
    },
  ],
};

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
  return <Line data={data} options={options} />;
};

export default LineChart;