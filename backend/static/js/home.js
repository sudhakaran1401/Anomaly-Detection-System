const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");

if (fileInput && fileName) {

    fileInput.addEventListener("change", function () {

        if (fileInput.files.length > 0) {

            fileName.style.display = "block";

            fileName.innerText =
                "Selected: " + fileInput.files[0].name;

        } else {

            fileName.style.display = "none";

            fileName.innerText = "";

        }

    });

}

function showLoader() {

    const loader = document.getElementById("loader");

    if (loader) {

        loader.style.display = "block";

    }

    const btn = document.getElementById("submitBtn");

    if (btn) {

        btn.disabled = true;

        btn.innerText = "Processing...";

    }

}