import {
    useEffect,
    useMemo,
    useState,
} from "react";

import { useTheme } from "../../components/ThemeContext";

import Pagination from "./Pagination";
import TableHeader from "../TableHeader";
import TableBody from "../TableBody";

export default function DataTable({
    rows = [],
}) {
    const { darkMode } = useTheme();

    const [currentPage, setCurrentPage] =
        useState(1);

    const [rowsPerPage, setRowsPerPage] =
        useState(5);

    useEffect(() => {
        setCurrentPage(1);
    }, [rows]);

    const columns = useMemo(() => {
        if (!rows.length) return [];
        return Object.keys(rows[0]);
    }, [rows]);

    const totalRows = rows.length;

    const currentRows = useMemo(() => {
        const start =
            (currentPage - 1) * rowsPerPage;

        return rows.slice(
            start,
            start + rowsPerPage
        );
    }, [
        rows,
        currentPage,
        rowsPerPage,
    ]);

    return (
        <div className="container mt-4">
            <div
                className={`card shadow-lg ${
                    darkMode
                        ? "theme-dark-card"
                        : "theme-light-card"
                }`}
            >
                <div className="table-responsive">
                    <table className="table table-bordered table-striped table-hover text-center align-middle mb-0">

                        <TableHeader
                            columns={columns}
                        />

                        <TableBody
                            rows={currentRows}
                            columns={columns}
                        />

                    </table>
                </div>

                <div
                    className={`card-body ${
                        darkMode
                            ? "theme-dark-card"
                            : "theme-light-card"
                    }`}
                >
                    <Pagination
                        totalRows={totalRows}
                        rowsPerPage={
                            rowsPerPage
                        }
                        currentPage={
                            currentPage
                        }
                        setCurrentPage={
                            setCurrentPage
                        }
                        setRowsPerPage={
                            setRowsPerPage
                        }
                    />
                </div>
            </div>
        </div>
    );
}