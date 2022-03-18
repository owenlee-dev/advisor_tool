import React, { useMemo, useState, useEffect, useContext } from "react";
import { Table, Button } from "react-bootstrap";
import TableScrollbar from "react-table-scrollbar";
import {
  useTable,
  useSortBy,
  useGlobalFilter,
  useRowSelect,
  useFilters,
  useAbsoluteLayout,
} from "react-table";
import "../../styles/MasterList.scss";
import DataContext from "../DataContext";
import api from "../../api/api";
import {
  fuzzyTextFilterFn,
  DefaultColumnFilter,
  GlobalFilter,
} from "./TableFilters";
import { columns } from "./Columns";
import { CheckBox } from "./CheckBox";

const MasterList = () => {
  const [data, setData] = useState([]);
  const { masterData, rankMethod } = useContext(DataContext);

  //set table values to the state master data
  useEffect(() => {
    if (masterData.length == 0) {
      const fetchData = async () => {
        const master = await api.getMasterList(rankMethod);
        setData(master);
      };
      fetchData();
    } else {
      setData(masterData);
    }
  }, [rankMethod]);

  const filterTypes = React.useMemo(
    () => ({
      // Add a new fuzzyTextFilterFn filter type.
      fuzzyText: fuzzyTextFilterFn,
      // Or, override the default text filter to use
      // "startWith"
      text: (rows, id, filterValue) => {
        return rows.filter((row) => {
          const rowValue = row.values[id];
          return rowValue !== undefined
            ? String(rowValue)
                .toLowerCase()
                .startsWith(String(filterValue).toLowerCase())
            : true;
        });
      },
    }),
    []
  );

  const defaultColumn = React.useMemo(
    () => ({
      // Let's set up our default Filter UI
      Filter: DefaultColumnFilter,
    }),
    []
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
    state,
    visibleColumns,
    preGlobalFilteredRows,
    setGlobalFilter,
  } = useTable(
    {
      columns,
      data,
      defaultColumn, // Be sure to pass the defaultColumn option
      filterTypes,
    },
    useFilters,
    useGlobalFilter,
    useSortBy,
    useRowSelect,
    (hooks) => {
      hooks.visibleColumns.push((columns) => {
        return [
          {
            id: "selection",
            Header: ({ getToggleAllRowsSelectedProps }) => (
              <div>
                <CheckBox {...getToggleAllRowsSelectedProps()} />
              </div> // check boxes on left handside of the student master list
            ),
            Cell: ({ row }) => (
              <CheckBox {...row.getToggleRowSelectedProps()} />
            ),
          },
          ...columns,
        ];
      });
    }
  );

  return (
    <>
      <div className="table-wrapper">
        <Table
          striped
          bordered
          hover
          className="masterlist"
          {...getTableProps()}
        >
          <thead>
            <tr>
              <th colSpan={visibleColumns.length}>
                <div className="table-settings">
                  <GlobalFilter
                    preGlobalFilteredRows={preGlobalFilteredRows}
                    globalFilter={state.globalFilter}
                    setGlobalFilter={setGlobalFilter}
                  />
                  <div>
                    <Button variant="secondary">Generate Text Audit</Button>
                    <Button variant="secondary">Generate Matrix Audit</Button>
                  </div>
                </div>
              </th>
            </tr>
            {headerGroups.map((headerGroup) => (
              <tr {...headerGroup.getHeaderGroupProps()}>
                {headerGroup.headers.map((column) => (
                  <th
                    className="table-header"
                    {...column.getHeaderProps(column.getSortByToggleProps())}
                  >
                    {column.render("Header")}
                    <span className="sort-text">
                      {column.isSorted ? (column.isSortedDesc ? "⟰" : "⟱") : ""}
                    </span>
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody {...getTableBodyProps()}>
            {rows.map((row) => {
              prepareRow(row);
              return (
                <tr {...row.getRowProps()}>
                  {row.cells.map((cell) => {
                    return (
                      <td {...cell.getCellProps()}>{cell.render("Cell")}</td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </Table>
      </div>
    </>
  );
};

export default MasterList;
