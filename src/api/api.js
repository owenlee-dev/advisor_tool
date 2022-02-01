import axios from "axios";

// This file is a layer of abstraction between the front end and the backend

const getMasterList = (rankMethod) => {
  const result = axios
    .get("/get_masterlist", { params: { rank_method: rankMethod } })
    .then((res) => {
      return res.data;
    });
  return result;
};

const uploadDataSet = (formData, setDataLoading) => {
  axios({
    url: "/upload_dataset",
    method: "POST",
    mode: "cors",
    headers: { "Content-Type": "multipart/form-data" },
    data: formData,
  })
    .then((res) => {
      setDataLoading(false);
      console.log(res);
    })
    .catch((err) => {
      console.error(err);
    });
};

const uploadConfigFile = (formData) => {
  axios({
    url: "/upload_config",
    method: "POST",
    mode: "cors",
    data: formData,
  })
    .then((res) => {
      console.log(res);
    })
    .catch((err) => {
      console.error(err);
    });
};

const uploadPrereqFile = (formData) => {
  axios({
    url: "/upload_prereq",
    method: "POST",
    mode: "cors",
    data: formData,
  })
    .then((res) => {
      console.log(res);
    })
    .catch((err) => {
      console.error(err);
    });
};

const checkForConfig = () => {
  const result = axios.get("/check_for_config").then((res) => {
    return res.data;
  });
  return result;
};

const checkForPrereq = () => {
  const result = axios.get("/check_for_prereq").then((res) => {
    return res.data;
  });
  return result;
};

const testFuncion = () => {
  const result = axios.get("/test_function").then((res) => {
    return res.data;
  });
  return result;
};

export default {
  getMasterList,
  uploadDataSet,
  uploadConfigFile,
  uploadPrereqFile,
  checkForPrereq,
  checkForConfig,
  testFuncion,
};
