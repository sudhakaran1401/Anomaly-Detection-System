export default function TableHeader({
    columns,
}) {
    return (
        <thead>
            <tr>
                {columns.map((column) => (
                    <th key={column}>
                        {column
                            .replaceAll("_", " ")
                            .replace(
                                /\b\w/g,
                                (c) => c.toUpperCase()
                            )}
                    </th>
                ))}
            </tr>
        </thead>
    );
}