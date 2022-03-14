import React, { useEffect, useState, useContext } from "react";
import { Container, Dropdown, DropdownButton, Row, Col } from "react-bootstrap";
import "../styles/Counts.scss";
import DataContext from "./DataContext";
import api from "../api/api";
import CountsChart from "./Tables/CountsChart";

const Counts = () => {
  const { rankMethod } = useContext(DataContext);
  const [countRangeParameter, setCountRangeParameter] = useState("Cohort");
  const [cohorts, setCohorts] = useState([
    "2020-2021",
    "2019-2020",
    "2018-2019",
    "2017-2018",
    "2016-2017",
    "2015-2016",
  ]);
  const [semesters, setSemesters] = useState([]);
  const [currentRange, setCurrentRange] = useState("2020-21");

  const [FIR, setFIR] = useState("0");
  const [SOP, setSOP] = useState("0");
  const [JUN, setJUN] = useState("0");
  const [SEN, setSEN] = useState("0");
  const [COOP, setCOOP] = useState("0");

  useEffect(() => {
    const getCounts = async () => {
      // need to pass this function the rankMethod
      let rankCounts = {};
      if (countRangeParameter == "Cohort") {
        rankCounts = await api.getCohortRankCounts(currentRange);
      } else {
        rankCounts = await api.getSemesterRankCounts(currentRange);
      }
      setFIR(rankCounts.FIR);
      setSOP(rankCounts.SOP);
      setJUN(rankCounts.JUN);
      setSEN(rankCounts.SEN);
    };
    getCounts();
  }, [currentRange]);
  // This will rerender counts when the page loads
  // or if the rank calc method, count range parameter or the range changes
  useEffect(() => {
    const getRanges = async () => {
      const rangeParameters = await api.getCountRanges();
      setCohorts(rangeParameters.cohorts);
      setSemesters(rangeParameters.semesters);
      if (countRangeParameter == "Cohort") {
        setCurrentRange(cohorts[0]);
      } else {
        setCurrentRange(semesters[0]);
      }
    };

    const getCoopCounts = async () => {
      const countTotals = await api.getCoopCounts(
        countRangeParameter,
        currentRange
      );
      setCOOP(countTotals);
    };

    getCoopCounts();
    getRanges();
  }, [rankMethod, countRangeParameter]);

  return (
    <Container fluid className="count-container">
      <Row className="buttons">
        <Col>
          <h2 className="help-text">Count students by: </h2>
          <DropdownButton
            variant="dark"
            size="sm"
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
        </Col>
        <Col>
          <h2 className="help-text">Students in {countRangeParameter}: </h2>
          <DropdownButton
            variant="dark"
            size="sm"
            className="range-dropdown"
            title={currentRange}
          >
            {countRangeParameter === "Cohort" &&
              cohorts.map((element) => (
                <Dropdown.Item
                  key={element}
                  variant="dark"
                  onClick={() => setCurrentRange(element)}
                >
                  {element}
                </Dropdown.Item>
              ))}
            {countRangeParameter != "Cohort" &&
              semesters.map((element) => (
                <Dropdown.Item
                  key={element}
                  variant="dark"
                  onClick={() => setCurrentRange(element)}
                >
                  {element}
                </Dropdown.Item>
              ))}
          </DropdownButton>
        </Col>
      </Row>
      <Row className="graph">
        <CountsChart FIR={FIR} SOP={SOP} JUN={JUN} SEN={SEN} />
      </Row>
      <Row className="totals">
        <h2 className="bot-help-text">
          Total Students: {FIR + SOP + JUN + SEN}
        </h2>
        <h2 className="bot-help-text">Students in Co-Op: {COOP}</h2>
      </Row>
    </Container>
  );
};
export default Counts;
