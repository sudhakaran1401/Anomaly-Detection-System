import { useEffect } from "react";

export default function Pagination({
    totalRows,
    rowsPerPage,
    currentPage,
    setCurrentPage,
    setRowsPerPage,
    hasNext = false,
    hasPrevious = false,
    serverSide = false,
}) {
    const totalPages = Math.max(
        1,
        Math.ceil(totalRows / rowsPerPage)
    );

    useEffect(() => {
        if (!serverSide && currentPage > totalPages) {
            setCurrentPage(totalPages);
        }
    }, [
        currentPage,
        totalPages,
        serverSide,
        setCurrentPage,
    ]);

    const startRow =
        totalRows === 0
            ? 0
            : (currentPage - 1) * rowsPerPage + 1;

    const endRow = Math.min(
        currentPage * rowsPerPage,
        totalRows
    );

    return (
        <div className="d-flex justify-content-between align-items-center flex-wrap mt-2">

            <div>

                <label>

                    Rows per page:

                </label>

                <select
                    className="form-select d-inline-block w-auto ms-2"
                    value={rowsPerPage}
                    onChange={(e) => {
                        setRowsPerPage(Number(e.target.value));
                        setCurrentPage(1);
                    }}
                >
                    <option value={5}>5</option>
                    <option value={10}>10</option>
                    <option value={15}>15</option>
                    <option value={20}>20</option>
                </select>

            </div>

            <div>

                <span>

                    Showing {startRow}-{endRow} of {totalRows}

                </span>

            </div>

            <div>

                <button
                    className="btn btn-primary btn-sm me-2"
                    disabled={
                        serverSide
                            ? !hasPrevious
                            : currentPage === 1
                    }
                    onClick={() =>
                        setCurrentPage(currentPage - 1)
                    }
                >
                    Previous
                </button>

                <button
                    className="btn btn-primary btn-sm"
                    disabled={
                        serverSide
                            ? !hasNext
                            : currentPage === totalPages
                    }
                    onClick={() =>
                        setCurrentPage(currentPage + 1)
                    }
                >
                    Next
                </button>

            </div>

        </div>
    );
}