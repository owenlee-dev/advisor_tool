import React, { useState, useMemo } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Route, Routes, BrowserRouter as Router } from "react-router-dom";
import Layout from "./components/Layout";
import Configuration from "./components/Configuration";
import Dashboard from "./components/Dashboard";
import DataContext from "./components/DataContext";

function App() {
  const [masterData, setMasterData] = useState([]);
  const [rankMethod, setRankMethod] = useState("Course");
  const [dataLoading, setDataLoading] = useState(false);

  // state management - useMemo used so that it only fetches when it needs to
  const providerValue = useMemo(
    () => ({
      masterData,
      setMasterData,
      rankMethod,
      setRankMethod,
      dataLoading,
      setDataLoading,
    }),
    [
      masterData,
      setMasterData,
      rankMethod,
      setRankMethod,
      dataLoading,
      setDataLoading,
    ]
  );

  // Function to register a user in the database
  const [key, setKey] = useState("dashboard");
  // const registerUser = () => {
  //   let formData = new FormData();
  //   formData.append("email", "tesst.test");
  //   formData.append("password", "gdd");

  //   axios({
  //     url: "/test_route",
  //     method: "GET",
  //     data: formData,
  //   })
  //     .then((res) => {
  //       console.log(res);
  //     })
  //     .catch((err) => {
  //       console.error(err);
  //     });
  // };

  return (
    <DataContext.Provider value={providerValue}>
      <Router>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="*" element={<Dashboard />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="configuration" element={<Configuration />} />
          </Route>
        </Routes>
      </Router>
    </DataContext.Provider>
  );
}

export default App;
