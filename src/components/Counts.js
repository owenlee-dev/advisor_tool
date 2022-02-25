import React, { useEffect, useState } from "react";
import { Container, Dropdown, DropdownButton, Row } from "react-bootstrap";
import "../styles/Counts.scss";
const Counts = () => {
  const [countRangeParameter, setCountRangeParameter] = useState("Cohort");
  return (
    <Container className="container">
      <Row className="buttons">
        <DropdownButton className="dataset" title="Cohort">
          <Dropdown.Item onClick={() => setCountRangeParameter("Cohort")}>
            Cohort
          </Dropdown.Item>
          <Dropdown.Item onClick={() => setCountRangeParameter("Semester")}>
            Semester
          </Dropdown.Item>
        </DropdownButton>
      </Row>
      <Row className="counts">
        <Row>FIR</Row>
        <Row>SOP</Row>
        <Row>JUN</Row>
        <Row>SEN</Row>
      </Row>
    </Container>
  );
};
export default Counts;
