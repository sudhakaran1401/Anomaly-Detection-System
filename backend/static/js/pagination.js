// ========================================
// Pagination State
// ========================================

let currentPage = 1;
let rowsPerPage = 5;


// ========================================
// Show Page
// ========================================

function showPage(page) {

    const table = document.getElementById("dataTable") || document.getElementById("historyTable");;

    const tbody = table.getElementsByTagName("tbody")[0];

    // ALL rows
    const allRows = Array.from(
        tbody.getElementsByTagName("tr")
    );

    // ONLY visible rows
    const visibleRows = allRows.filter(
        row => row.dataset.visible !== "false"
    );

    const totalRows = visibleRows.length;

    const totalPages =
        Math.ceil(totalRows / rowsPerPage) || 1;

    // Prevent invalid pages
    if (page < 1) page = 1;

    if (page > totalPages) page = totalPages;

    currentPage = page;

    // ====================================
    // Reset ALL rows first
    // ====================================

    allRows.forEach(row => {
        row.style.display = "none";
    });

    // ====================================
    // Pagination Slice
    // ====================================

    const start =
        (currentPage - 1) * rowsPerPage;

    const end = start + rowsPerPage;

    // Show current page rows
    for (
        let i = start;
        i < end && i < totalRows;
        i++
    ) {
        visibleRows[i].style.display = "";
    }

    // ====================================
    // Update Footer
    // ====================================

    document.getElementById("pageInfo").innerText =
        `Page ${currentPage} of ${totalPages}`;

    document.getElementById("prevBtn").disabled =
        currentPage === 1;

    document.getElementById("nextBtn").disabled =
        currentPage === totalPages;
}


// ========================================
// Change Rows Per Page
// ========================================

function changeRowsPerPage() {

    rowsPerPage = parseInt(
        document.getElementById("rowsSelect").value
    );

    currentPage = 1;

    showPage(currentPage);
}


// ========================================
// Next Page
// ========================================

function nextPage() {
    showPage(currentPage + 1);
}


// ========================================
// Previous Page
// ========================================

function prevPage() {
    showPage(currentPage - 1);
}


// ========================================
// Filter Table
// ========================================

function filterTable(type) {

    const rows = document.querySelectorAll(
        "#dataTable tbody tr"
    );

    rows.forEach(row => {

        const resultCell = row.querySelector(
            ".result-cell"
        );

        const result = resultCell
            ? resultCell.innerText.trim().toLowerCase()
            : "";

        // Show ALL
        if (type === "all") {

            row.dataset.visible = "true";

        } else {

            row.dataset.visible =
                result === type.toLowerCase()
                ? "true"
                : "false";
        }
    });

    currentPage = 1;

    showPage(currentPage);
}


// ========================================
// Search Table
// ========================================

function searchTable() {

    const search = document
        .getElementById("searchInput")
        .value
        .toLowerCase();

    const rows = document.querySelectorAll(
        "#dataTable tbody tr"
    );

    rows.forEach(row => {

        const text = row.innerText.toLowerCase();

        row.dataset.visible =
            text.includes(search)
            ? "true"
            : "false";
    });

    currentPage = 1;

    showPage(currentPage);
}


// ========================================
// Reset Filters
// ========================================

function resetTable() {

    const rows = document.querySelectorAll(
        "#dataTable tbody tr"
    );

    rows.forEach(row => {
        row.dataset.visible = "true";
    });

    document.getElementById("searchInput").value = "";

    currentPage = 1;

    showPage(currentPage);
}


// ========================================
// Initial Setup
// ========================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const rows = document.querySelectorAll(
            "#dataTable tbody tr"
        );

        // Default all rows visible
        rows.forEach(row => {
            row.dataset.visible = "true";
        });

        showPage(1);
    }
);