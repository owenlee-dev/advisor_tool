import React from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
} from "chart.js";
import { Bar } from "react-chartjs-2";
const CountsChart = (props) => {
  const { FIR, SOP, JUN, SEN } = props;
  const rankData = [FIR, SOP, JUN, SEN];
  const labels = [
    "FIR:\t\t" + FIR,
    "SOP:\t\t" + SOP,
    "JUN:\t\t" + JUN,
    "SEN:\t\t" + SEN,
  ];
  ChartJS.register(CategoryScale, LinearScale, BarElement);

  const options = {
    indexAxis: "y",
    scales: {
      x: {
        ticks: {
          align: "start",
          color: "black",
        },
      },
    },
    elements: {
      bar: {
        borderWidth: 2,
      },
    },
    responsive: true,
  };

  const data = {
    labels,
    datasets: [
      {
        data: rankData,
        borderColor: "#30100E",
        backgroundColor: "#F08D84",
      },
    ],
  };

  return <Bar options={options} data={data} />;
};

export default CountsChart;
