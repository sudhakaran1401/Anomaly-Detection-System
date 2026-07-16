export default function TableBody({
    rows,
    columns,
}) {
    if (!rows.length) {
        return (
            <tbody>
                <tr>
                    <td
                        colSpan={
                            columns.length || 1
                        }
                        className="text-center"
                    >
                        No records found.
                    </td>
                </tr>
            </tbody>
        );
    }

    return (
        <tbody>
            {rows.map((row, rowIndex) => (
                <tr
                    key={rowIndex}
                    className={
                        row.result === "Anomaly"
                            ? "table-danger fw-bold"
                            : ""
                    }
                >
                    {columns.map((column) => (
                        <td key={column}>
                            {column === "result" ? (
                                row[column] ===
                                "Anomaly" ? (
                                    <span className="badge bg-danger">
                                        Anomaly
                                    </span>
                                ) : (
                                    <span className="badge bg-success">
                                        Normal
                                    </span>
                                )
                            ) : typeof row[
                                  column
                              ] === "number" ? (
                                Number(
                                    row[column]
                                ).toFixed(3)
                            ) : (
                                String(
                                    row[column]
                                )
                            )}
                        </td>
                    ))}
                </tr>
            ))}
        </tbody>
    );
}