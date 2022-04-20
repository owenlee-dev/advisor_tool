import React, { useMemo, useState, useEffect, useContext } from "react";
import { Table, Button } from "react-bootstrap";
import { useTable, useRowSelect } from "react-table";
import "../../styles/AuditTable.scss";
import DataContext from "../DataContext";
import { columns } from "./AuditColumns";

const AuditTable = (props) => {
  let currentType = props.currentType;
  let data = props.data;
  const { rankMethod } = useContext(DataContext);
  // Function to set the table data each time the drop down changes
  // data needs to be of form: [{term: xyz, course_id: zyx, grade: A+}]

  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } =
    useTable(
      {
        columns,
        data,
      },
      useRowSelect
    );

  return (
    <div className="audit-table">
      <Table striped bordered {...getTableProps()}>
        <thead className="table-header">
          {headerGroups.map((headerGroup) => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map((column) => (
                <th {...column.getHeaderProps()}>{column.render("Header")}</th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {rows.map((row, i) => {
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
  );
};

export default AuditTable;
