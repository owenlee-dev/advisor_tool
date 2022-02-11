import React, { useEffect, useState, useContext } from "react";
import MasterList from "./MasterList";
import {
  Container,
  Row,
  Col,
  Dropdown,
  DropdownButton,
  Item,
  Button,
} from "react-bootstrap";
import DataContext from "./DataContext";
import api from "../api/api";
import "../styles/Dashboard.scss";

const Dashboard = () => {
  const { masterData, changeMasterData, rankMethod, setRankMethod } =
    useContext(DataContext);

  //set drop down state from backend
  useEffect(() => {
    const persistDropdowns = async () => {
      const stateFromBe = await api.getGlobalState();
      setRankMethod(stateFromBe.rankMethod);
    };
    persistDropdowns();
  }, []);

  const changeRankMethod = async (newRank) => {
    let formData = new FormData();
    formData.append("rankMethod", newRank);
    api.setGlobalRank(formData);
    setRankMethod(newRank);
  };
  //set it so that the rank method is stoerd and fetched from the backend so that it can be rerendered and also persists after refresh
  return (
    <Container fluid className="dashboard-container">
      <div className="border">
        <Row>
          <Col className="setting-container">
            <div className="btn-container">
              <DropdownButton className="dataset" title="BSSWE">
                <Dropdown.Item onClick={() => setRankMethod("Course")}>
                  BSSWE
                </Dropdown.Item>
                <Dropdown.Item onClick={() => setRankMethod("Credit Hours")}>
                  BSECE
                </Dropdown.Item>
              </DropdownButton>
            </div>
            <div className="btn-container">
              <DropdownButton className="dataset" title={rankMethod}>
                <Dropdown.Item onClick={() => changeRankMethod("Course")}>
                  Courses
                </Dropdown.Item>
                <Dropdown.Item onClick={() => changeRankMethod("Credit Hours")}>
                  Credit Hours
                </Dropdown.Item>
              </DropdownButton>
            </div>
            <div className="btn-container">
              <Button onClick={() => api.testFuncion()}>TEST</Button>
            </div>
          </Col>
        </Row>
        <Row>
          <Col className="count-container">
            <Row className="count-row">COUNTS</Row>
            <Row className="count-row">AUDIT</Row>
          </Col>
          <Col className="list-container">
            <MasterList />
          </Col>
        </Row>
      </div>
    </Container>
  );
};

export default Dashboard;
