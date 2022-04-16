import {
  SelectColumnFilter,
  compareCourseCode,
  compareRank,
} from "./TableFilters";

export const columns = [
  {
    Header: "Student ID  ",
    accessor: "student_id",
  },
  {
    Header: "Name  ",
    accessor: "name",
  },
  {
    Header: "Rank  ",
    accessor: "rank",
    sortType: compareRank,
    Filter: SelectColumnFilter,
  },
  {
    Header: "Status  ",
    accessor: "status",
    Filter: SelectColumnFilter,
  },
  {
    Header: "Campus  ",
    accessor: "campus",
    Filter: SelectColumnFilter,
    filter: "includes",
  },
];

export const AuditColumns = [
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
