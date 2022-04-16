import React, { useMemo, useState, useEffect, useContext } from "react";
import { Table, Button } from "react-bootstrap";
import {
  useTable,useRowSelect,
} from "react-table";
import "../../styles/MasterList.scss";
import DataContext from "../DataContext";
import api from "../../api/api";
import { AuditColumns } from "./Columns";

const AuditTable = () => {
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

 
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable(
    {
      AuditColumns,
      data,
    },
    useRowSelect
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

export default AuditTable;
