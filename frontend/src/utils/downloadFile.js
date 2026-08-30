export function downloadFile(
    response,
    defaultFilename,
    mimeType
) {
    const blob = new Blob([response.data], {
        type: mimeType,
    });

    const url = URL.createObjectURL(blob);

    const disposition =
        response.headers["content-disposition"];

    let filename = defaultFilename;

    if (disposition) {

        const match =
            disposition.match(
                /filename="?([^"]+)"?/
            );

        if (match) {
            filename = match[1];
        }

    }

    const link =
        document.createElement("a");

    link.href = url;

    link.download = filename;

    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);

    URL.revokeObjectURL(url);
}