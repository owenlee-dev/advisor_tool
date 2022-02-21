import React, { useState, useEffect, useContext } from "react";
import "../styles/Configuration.scss";
import {
  Button,
  DropdownButton,
  Dropdown,
  Card,
  Form,
  Spinner,
} from "react-bootstrap";
import api from "../api/api";
import DataContext from "./DataContext";

/**
TODO Give live updates about load and extraction of data
TODO Workshop messages to the user to add clarity 
TODO add ability to set the data set that you would like to see
*/

const Configuration = () => {
  const {
    masterData,
    setMasterData,
    rankMethod,
    setRankMethod,
    dataLoading,
    setDataLoading,
  } = useContext(DataContext);

  const [personData, setPersonData] = useState();
  const [courseData, setCourseData] = useState();
  const [transferData, setTransferData] = useState();
  const [configFile, setConfigFile] = useState();
  const [prereqFile, setPrereqFile] = useState();
  const [prereqLoaded, setPrereqLoaded] = useState(false);
  const [configLoaded, setConfigLoaded] = useState(false);

  // checking if the prereq/config files are already loaded into the system
  useEffect(() => {
    const fetchData = async () => {
      const prereqRes = api.checkForPrereq().then((res) => {
        setPrereqLoaded(res);
      });
      const configRes = api.checkForConfig().then((res) => {
        setConfigLoaded(res);
      });
    };
    fetchData();
  }, []);

  //Function to set file states equal to file contents
  const dataSetChangeHandler = (event) => {
    const files = event.target.files;
    for (let i = 0; i < files.length; i++) {
      if (files[i].name == "courseData.txt") {
        setCourseData(files[i]);
      } else if (files[i].name == "personData.txt") {
        setPersonData(files[i]);
      } else if (files[i].name == "transferData.txt") {
        setTransferData(files[i]);
      } else {
        console.error("Unknown file name present");
      }
    }
  };

  //Function to set file state equal to uploaded file contents
  const configChangeHandler = (event) => {
    setConfigFile(event.target.files[0]);
  };
  //Function to set file state equal to uploaded file contents
  const prereqChangeHandler = (event) => {
    setPrereqFile(event.target.files[0]);
  };

  //function to receive the data files and pass them to the backend
  const handleDataSetSubmit = async (event) => {
    event.preventDefault();
    let formData = new FormData();
    formData.append("personData", personData);
    formData.append("courseData", courseData);
    formData.append("transferData", transferData);
    //make api call
    setDataLoading(true);
    api.uploadDataSet(formData, setDataLoading);

    //set state
    api.getMasterList(rankMethod).then((res) => {
      setMasterData(res);
    });
  };

  //function to receive the config file and pass them to the backend
  const handleConfigSubmit = (event) => {
    // event.preventDefault();
    let formData = new FormData();
    formData.append("configFile", configFile);
    //make api call
    api.uploadConfigFile(formData);
  };

  //function to receive the prereq file and pass them to the backend
  const handlePrereqSubmit = (event) => {
    // event.preventDefault();
    let formData = new FormData();
    formData.append("prereqFile", prereqFile);
    //make api call
    api.uploadPrereqFile(formData);
  };

  //TEST FUNCTIONS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  const testPress = () => {
    console.log(dataLoading);
  };

  //NESTED COMPONENTS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  const ErrorMessage = (props) => {
    const { msg } = props;
    return <Card.Text className="error-txt">{msg}</Card.Text>;
  };

  return (
    <div className="upload-container">
      <Card border="secondary" className="upload-card">
        <Card.Header>
          <h2>Data Set</h2>
        </Card.Header>

        {!prereqLoaded && <ErrorMessage msg="Missing Prerequisite File" />}
        {!configLoaded && <ErrorMessage msg="Missing Configuration File" />}

        <Card.Body className="card-body">
          Upload a set of three text files. Select a data set and load it in
          with the set button.
          <Form onSubmit={handleDataSetSubmit} className="card-form">
            <Form.Control
              type="file"
              multiple
              onChange={dataSetChangeHandler}
            />
            <div className="btn-spinner">
              {prereqLoaded && configLoaded && (
                <Button className="btn upload" type="submit">
                  Upload
                </Button>
              )}
              {(!prereqLoaded || !configLoaded) && (
                <Button className="btn upload" type="submit" disabled>
                  Upload
                </Button>
              )}
              {dataLoading && (
                <Spinner className="spinner" animation="border" />
              )}
            </div>
          </Form>
        </Card.Body>
      </Card>
      <Card border="secondary" className="upload-card">
        <Card.Header>
          <h2>Configuration File</h2>
        </Card.Header>
        <Card.Body className="card-body">
          Upload a new XML configuration file
          <Form onSubmit={handleConfigSubmit} className="card-form">
            <Form.Control type="file" onChange={configChangeHandler} />
            <Button className="btn upload" type="submit">
              Upload
            </Button>
          </Form>
        </Card.Body>
      </Card>

      {/* Has not yet been hooked up to accept file input */}
      <Card border="secondary" className="upload-card">
        <Card.Header>
          <h2>Rank Prerequisites</h2>
        </Card.Header>
        <Card.Body className="card-body">
          Select rank calculation method and upload the configuration file
          <Form onSubmit={handlePrereqSubmit} className="card-form">
            <Form.Control type="file" onChange={prereqChangeHandler} />
            <Button className="btn upload" type="submit">
              Upload
            </Button>
          </Form>
        </Card.Body>
      </Card>

      {/* <Card className="upload-card">
        <Card.Header>
          <h2>Test Card</h2>
        </Card.Header>
        <Button onClick={testPress}>TEST</Button>
      </Card> */}
    </div>
  );
};

export default Configuration;
