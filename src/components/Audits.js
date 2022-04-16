import { computeHeadingLevel } from "@testing-library/react";
import { React,useState } from "react";
import api from "../api/api";
import "../styles/Audits.scss";
import {
    Container,
    Row,
    Col,
    Button,
    DropdownButton
  } from "react-bootstrap";
import AuditTable from "./Tables/AuditTable"


const Audits = () => {

  const [selectedStudent, setSelectedStudent]=useState("Fletcher Donaldson")

  const testButtonClick=async ()=>{
      let auditObject=await api.auditStudent('5091054')
      console.log(auditObject)
  }



  return (
  <Container className="audit-container">
    <Button onClick={testButtonClick}>TEST</Button>
    <Row>{selectedStudent}</Row>
    <Row>
      <Col>
        <DropdownButton title="Type"></DropdownButton>
      </Col>
      <Col>
        <Row>Total Needed: 4</Row>
        <Row>Total Passed: 4</Row>
        <Row>Total in Progress: 4</Row>
      </Col>
    </Row>
    <Row>
      <AuditTable />
    </Row>
  </Container>)
};
export default Audits;
