import React from "react";

export default function BaseChart({
    ChartComponent,
    data,
    options,
}) {
    return (
        <div className="chart-wrapper">
            <ChartComponent
                data={data}
                options={options}
            />
        </div>
    );
}