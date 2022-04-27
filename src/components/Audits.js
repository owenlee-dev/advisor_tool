import { React, useState, useEffect, useContext } from "react";
import api from "../api/api";
import "../styles/Audits.scss";
import {
  Container,
  Row,
  Col,
  Button,
  DropdownButton,
  Dropdown,
  Item,
} from "react-bootstrap";
import DataContext from "./DataContext";
import AuditTable from "./Tables/AuditTable";

const Audits = () => {
  const [currentAuditTable, setCurrentAuditTable] = useState("ALL");
  const [data, setData] = useState([]);
  const [totalNeeded, setTotalNeeded] = useState(0);
  const [totalPassed, setTotalPassed] = useState(0);
  const [totalIP, setTotalIP] = useState(0);

  const { audit, setAudit, selectedStudent } = useContext(DataContext);

  const getSelectedStudent = () => {
    let selectedStudentOBJ = { name: "No Student Found" };
    if (selectedStudent) {
      selectedStudentOBJ = JSON.parse(selectedStudent);
    }
    return selectedStudentOBJ.name;
  };

  // function to get course that are currently in progress
  const getCoursesIP = () => {
    let allCoursesIP = [];
    let coursesIP = [];
    Object.values(audit.courses_taken).forEach((course) => {
      if (
        course.grade === "" &&
        (course.course_type === currentAuditTable ||
          currentAuditTable === "ALL")
      ) {
        coursesIP.push(course);
      }
    });
    return coursesIP;
  };
  // get audit object
  // fetch new audit object when new student gets selected
  useEffect(() => {
    console.log(audit);
    const fetchAudit = async () => {
      if (selectedStudent) {
        const auditObject = await api.auditStudent(
          JSON.parse(selectedStudent).student_id
        );
        setAudit(auditObject);
        // console.log(audit);
      }
    };
    fetchAudit();
  }, [selectedStudent]);

  // set table contents when new student is selected or course type is changed
  useEffect(() => {
    if (Object.keys(audit).length > 0) {
      let allCoursesTaken = Object.values(audit.courses_taken);
      let forTableData = [];
      if (currentAuditTable === "ALL") {
        setData(allCoursesTaken);
      } else {
        for (let i = 0; i < allCoursesTaken.length; i++) {
          if (allCoursesTaken[i].course_type === currentAuditTable) {
            forTableData.push(allCoursesTaken[i]);
          }
        }
        setData(forTableData);
      }
      setTotalNeeded(audit.course_type_needed[currentAuditTable]);
      setTotalPassed(audit.course_type_taken[currentAuditTable]);
      setTotalIP(getCoursesIP().length);
    }
  }, [audit, currentAuditTable]);

  return (
    <Container className="audit-container">
      <Row className="student-name">{getSelectedStudent()}</Row>
      <Row className="totals-row">
        <Col md={4} className="btn-col">
          <h2 className="help-text">Course Type</h2>
          <DropdownButton variant="dark" size="sm" title={currentAuditTable}>
            <Dropdown.Item onClick={() => setCurrentAuditTable("ALL")}>
              ALL
            </Dropdown.Item>
            <Dropdown.Item onClick={() => setCurrentAuditTable("CORE")}>
              CORE
            </Dropdown.Item>
            <Dropdown.Item onClick={() => setCurrentAuditTable("TE")}>
              TE
            </Dropdown.Item>
            <Dropdown.Item onClick={() => setCurrentAuditTable("BASSCI")}>
              BASSCI
            </Dropdown.Item>
            <Dropdown.Item onClick={() => setCurrentAuditTable("CSE-ITS")}>
              CSE-ITS
            </Dropdown.Item>
            <Dropdown.Item onClick={() => setCurrentAuditTable("CSE-HSS")}>
              CSE-HSS
            </Dropdown.Item>
            <Dropdown.Item onClick={() => setCurrentAuditTable("CSE-OPEN")}>
              CSE-OPEN
            </Dropdown.Item>
            <Dropdown.Item onClick={() => setCurrentAuditTable("EXTRA")}>
              EXTRA
            </Dropdown.Item>
          </DropdownButton>
        </Col>
        <Col md={8}>
          <table className="total-table">
            <tbody>
              <tr>
                <td>Total Needed:</td>
                <td>{totalNeeded}</td>
              </tr>
              <tr>
                <td>Total Passed</td>
                <td>{totalPassed}</td>
              </tr>
              <tr>
                <td>Total in Progress:</td>
                <td>{totalIP}</td>
              </tr>
            </tbody>
          </table>
        </Col>
      </Row>
      <Row>
        <AuditTable data={data} currentType={currentAuditTable} />
      </Row>
    </Container>
  );
};
export default Audits;
