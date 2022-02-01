import React, { useMemo, useState, useEffect, useContext } from "react";
import { Table, Button } from "react-bootstrap";
import TableScrollbar from "react-table-scrollbar";
import { useTable } from "react-table";
import "../styles/MasterList.scss";
import DataContext from "./DataContext";
import api from "../api/api";

const MasterList = () => {
  const [data, setData] = useState([]);
  const { masterData, setMasterData, rankMethod } = useContext(DataContext);

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
  }, []);

  const columns = useMemo(
    () => [
      {
        Header: "Student ID",
        accessor: "student_id",
      },
      {
        Header: "Name",
        accessor: "name",
      },
      {
        Header: "Program",
        accessor: "program",
      },
      {
        Header: "Campus",
        accessor: "campus",
      },
      {
        Header: "Rank",
        accessor: "rank",
      },
      {
        Header: "Status",
        accessor: "status",
      },
    ],
    []
  );

  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } =
    useTable({ columns, data });

  return (
    <>
      <TableScrollbar>
        <Table
          striped
          bordered
          hover
          className="masterlist"
          {...getTableProps()}
        >
          <thead className="header">
            {headerGroups.map((headerGroup) => (
              <tr {...headerGroup.getHeaderGroupProps()}>
                {headerGroup.headers.map((column) => (
                  <th {...column.getHeaderProps()}>
                    {column.render("Header")}
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
      </TableScrollbar>
    </>
  );
};

export default MasterList;
