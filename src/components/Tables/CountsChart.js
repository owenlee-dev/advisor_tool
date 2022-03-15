import React from "react";
import { Chart, CategoryScale, LinearScale, BarElement } from "chart.js";
import { Bar } from "react-chartjs-2";
import "../../styles/Counts.scss";

Chart.defaults.font.size = 17;
Chart.defaults.font.weight = 500;
Chart.defaults.font.family = "Open Sans";

const CountsChart = (props) => {
  const { FIR, SOP, JUN, SEN } = props;
  const rankData = [FIR, SOP, JUN, SEN];
  const labels = [
    "FIR:\t\t" + FIR,
    "SOP:\t\t" + SOP,
    "JUN:\t\t" + JUN,
    "SEN:\t\t" + SEN,
  ];
  Chart.register(CategoryScale, LinearScale, BarElement);

  const options = {
    indexAxis: "y",
    scales: {
      x: {
        ticks: {
          display: false,
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
