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

const getGlobalState = () => {
  const result = axios.get("/get_app_state").then((res) => {
    return res.data;
  });
  return result;
};

const setGlobalRank = (formData) => {
  axios({
    url: "/set_global_rank",
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
    .then((res) => {})
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

const getCountRanges = () => {
  const result = axios.get("/get_count_ranges").then((res) => {
    return res.data;
  });
  return result;
};

const getCohortRankCounts = (range) => {
  if (!range) {
    range = "2020-21";
  }
  const result = axios
    .get("/get_cohort_rank_counts", { params: { rangeParameter: range } })
    .then((res) => {
      return res.data;
    });
  return result;
};

const getSemesterRankCounts = (range) => {
  if (!range) {
    return null;
  }
  const result = axios
    .get("/get_semester_rank_counts", { params: { rangeParameter: range } })
    .then((res) => {
      return res.data;
    });
  return result;
};

const getCoopCounts = (type, range) => {
  if (!range) {
    return null;
  }
  const result = axios
    .get("/get_coop_counts", {
      params: { type, range },
    })
    .then((res) => {
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
  getGlobalState,
  setGlobalRank,
  uploadDataSet,
  uploadConfigFile,
  uploadPrereqFile,
  checkForPrereq,
  checkForConfig,
  getCountRanges,
  getCohortRankCounts,
  getSemesterRankCounts,
  getCoopCounts,
  testFuncion,
};
