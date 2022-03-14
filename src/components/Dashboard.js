import React, { useEffect, useState, useContext } from "react";
import MasterList from "./Tables/MasterList";
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
import Counts from "./Counts";

/**
 * Question for Dawn
 * Where should the data set be selectable
 * What should be the identified for these selectable datasets?
 * Should it be the upload date? start date range? etc
 */

const Dashboard = () => {
  const { masterData, rankMethod, setRankMethod } = useContext(DataContext);

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
  // Row = 12 cols or 100%
  return (
    <Container fluid className="dashboard-container">
      <Row>
        <Col className="col-1"></Col>
        <Col className="setting-container">
          <div className="btn-container">
            <DropdownButton
              variant="outline-light"
              className="dataset"
              title="BSSWE"
            >
              <Dropdown.Item onClick={() => setRankMethod("Course")}>
                BSSWE
              </Dropdown.Item>
              <Dropdown.Item onClick={() => setRankMethod("Credit Hours")}>
                BSECE
              </Dropdown.Item>
            </DropdownButton>
          </div>
          <div className="btn-container">
            <DropdownButton
              variant="outline-light"
              className="dataset"
              title={rankMethod}
            >
              <Dropdown.Item onClick={() => changeRankMethod("Course")}>
                Courses
              </Dropdown.Item>
              <Dropdown.Item onClick={() => changeRankMethod("Credit Hours")}>
                Credit Hours
              </Dropdown.Item>
            </DropdownButton>
          </div>
          <div className="btn-container">
            <Button variant="outline-light" onClick={() => api.testFuncion()}>
              TEST
            </Button>
          </div>
        </Col>
        <Col className="col-1"></Col>
      </Row>
      <Row>
        <Col className="col-1"></Col>
        <Col className="col-3 count-audit-col">
          <Row className="count-row">
            <Counts />
          </Row>
          <Row className="audit-row">AUDIT</Row>
        </Col>
        <Col className="col-7 list-container">
          <MasterList />
        </Col>
        <Col className="col-1"></Col>
      </Row>
    </Container>
  );
};

export default Dashboard;
