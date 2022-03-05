import React, { useEffect, useState,useContext } from "react";
import { Container, Dropdown, DropdownButton, Row, Col } from "react-bootstrap";
import "../styles/Counts.scss";
import DataContext from "./DataContext";
import api from "../api/api";
const Counts = () => {
  const {rankMethod} = useContext(DataContext);
  const [countRangeParameter, setCountRangeParameter] = useState("Cohort");
  const [FIR, setFIR] = useState("0");
  const [SOP, setSOP] = useState("0");
  const [JUN, setJUN] = useState("0");
  const [SEN, setSEN] = useState("0");

  useEffect(() => {
    const getCounts = async () => {
      // need to pass this function the rankMethod 
      const rankCounts = await api.getCohortRankCounts();
      setFIR(rankCounts.FIR);
      setSOP(rankCounts.SOP);
      setJUN(rankCounts.JUN);
      setSEN(rankCounts.SEN);

    };
    getCounts();
  }, [rankMethod]);

  return (
    <Container fluid className="count-container">
      <Col>
        <Row className="buttons">
          <DropdownButton
            className="count-range-dropdown"
            title={countRangeParameter}
          >
            <Dropdown.Item onClick={() => setCountRangeParameter("Cohort")}>
              Cohort
            </Dropdown.Item>
            <Dropdown.Item onClick={() => setCountRangeParameter("Semester")}>
              Semester
            </Dropdown.Item>
          </DropdownButton>
        </Row>
        <Row className="counts">
          <Row>FIR : {FIR}</Row>
          <Row>SOP : {SOP}</Row>
          <Row>JUN : {JUN}</Row>
          <Row>SEN : {SEN}</Row>
        </Row>
      </Col>
    </Container>
  );
};
export default Counts;
