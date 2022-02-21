import React from "react";
import { matchSorter } from "match-sorter";

// compare course code function
// in code EMGG*1015
// have to trim the "ENGG" part and
export function compareCourseCode(rowA, rowB, id, desc) {
  let arr_A = rowA.values[id];
  arr_A = arr_A.split("*"); // delimator for the scode string

  let arr_B = rowB.values[id];

  arr_B = arr_B.split("*");

  let a = Number.parseFloat(arr_A[1]);
  let b = Number.parseFloat(arr_B[1]);
  if (Number.isNaN(a)) {
    // Blanks and non-numeric strings to bottom
    a = desc ? Number.NEGATIVE_INFINITY : Number.POSITIVE_INFINITY;
  }
  if (Number.isNaN(b)) {
    b = desc ? Number.NEGATIVE_INFINITY : Number.POSITIVE_INFINITY;
  }
  if (a > b) return 1;
  if (a < b) return -1;
  return 0;
}

// tudent rank function for sorting the rank properly
// FIR->SOP->JUN->SEN
export function compareRank(rowA, rowB, id, desc) {
  let arr_A = rowA.values[id];
  let arr_B = rowB.values[id];
  let a = 0;
  let b = 0;

  if (arr_A === "SOP") {
    a = 1;
  } else if (arr_A === "JUN") {
    a = 2;
  } else if (arr_A === "SEN") {
    a = 3;
  }

  if (arr_B === "SOP") {
    b = 1;
  } else if (arr_B === "JUN") {
    b = 2;
  } else if (arr_B === "SEN") {
    b = 3;
  }

  if (Number.isNaN(a)) {
    // Blanks and non-numeric strings to bottom
    a = desc ? Number.NEGATIVE_INFINITY : Number.POSITIVE_INFINITY;
  }
  if (Number.isNaN(b)) {
    b = desc ? Number.NEGATIVE_INFINITY : Number.POSITIVE_INFINITY;
  }
  if (a > b) return 1;
  if (a < b) return -1;
  return 0;
}

// Define a filter for greater than
export function filterGreaterThan(rows, id, filterValue) {
  return rows.filter((row) => {
    const rowValue = row.values[id];
    return rowValue >= filterValue;
  });
}

// used for the default column filter
// param: column object
//
export function DefaultColumnFilter({
  column: { filterValue, preFilteredRows, setFilter },
}) {
  return (
    <input
      value={filterValue || ""}
      onChange={(e) => {
        setFilter(e.target.value || undefined); // Set undefined to remove the filter entirely
      }}
      placeholder={`Search Records...`}
    />
  );
}

// This is a custom filter UI for selecting
// a unique option from a list
export function SelectColumnFilter({
  column: { filterValue, setFilter, preFilteredRows, id },
}) {
  // Calculate the options for filtering
  // using the preFilteredRows
  const options = React.useMemo(() => {
    const options = new Set();
    preFilteredRows.forEach((row) => {
      options.add(row.values[id]);
    });
    return [...options.values()];
  }, [id, preFilteredRows]);

  // Render a multi-select box
  return (
    <select
      value={filterValue}
      onChange={(e) => {
        setFilter(e.target.value || undefined);
      }}
    >
      <option value="">All</option>
      {options.map((option, i) => (
        <option key={i} value={option}>
          {option}
        </option>
      ))}
    </select>
  );
}

// fuzzy text filtering function, allows for search for substring
// param: rows object, id
export function fuzzyTextFilterFn(rows, id, filterValue) {
  return matchSorter(rows, filterValue, { keys: [(row) => row.values[id]] });
}
