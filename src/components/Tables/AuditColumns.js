import {
  SelectColumnFilter,
  compareCourseCode,
  compareRank,
} from "./TableFilters";

export const columns = [
  {
    Header: "Term",
    accessor: "term",
  },
  {
    Header: "Course ID",
    accessor: "course_id",
  },
  {
    Header: "Grade",
    accessor: "grade",
  },
];
