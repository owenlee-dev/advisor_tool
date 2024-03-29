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
import Audits from "./Audits";
import AuditTable from "./Tables/AuditTable";

/**
 * Question for Dawn
 * Where should the data set be selectable
 * What should be the identified for these selectable datasets?
 * Should it be the upload date? start date range? etc
 *
 * Add text to dropdown for rank calculation
 * --> Rank by Credit Hour
 * --> Rank by Prereqs
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
      <Row className="sub-header">
        <Col className="col-1"></Col>
        <Col className="setting-container">
          <div className="btn-container">
            <DropdownButton
              variant="outline-light"
              className="dataset"
              title="Dataset"
            >
              <Dropdown.Item onClick={() => setRankMethod("Course")}>
                Dataset 1
              </Dropdown.Item>
              <Dropdown.Item onClick={() => setRankMethod("Credit Hours")}>
                Dataset 2
              </Dropdown.Item>
            </DropdownButton>
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
        </Col>
        <Col className="col-1"></Col>
      </Row>
      <Row className="console-content">
        <Col className="col-3 count-audit-col">
          <div className="count-row">
            <Counts />
          </div>
          <div className="audit-row">
            <Audits />
          </div>
        </Col>
        <Col className="col-7 list-container">
          <MasterList />
        </Col>
      </Row>
    </Container>
  );
};

export default Dashboard;
