import React, { useEffect, useContext } from "react";
import MasterList from "./MasterList";
import { Container, Row, Col } from "react-bootstrap";
import DataContext from "./DataContext";

import "../styles/Dashboard.scss";

const Dashboard = () => {
  const { masterData, changeMasterData } = useContext(DataContext);

  return (
    <Container fluid className="dashboard-container">
      <Row>
        <Col className="count-container">COUNTS</Col>
        <Col className="table-container">
          <MasterList />
        </Col>
      </Row>
    </Container>
  );
};

export default Dashboard;
