
function startDynamicAnalyze() {
    let file = document.getElementById("file-selection");
    file = file.options[file.selectedIndex].value;

    let systemType = document.getElementById("os-selection");
    systemType = systemType.options[systemType.selectedIndex].text;

    if (!file) {
        alert("Выберите файл для проверки!");
    } else if (systemType === "Выберите ОС") {
        alert("Выберите ОС, на которой будет проверяться файл");
    } else {
        console.log("do something...");
        console.log(systemType);
        console.log(file);
    }
}

async function getFilesFromServer() {
    const fileSelect = document.getElementById("file-selection");

    const headers = new Headers();


    const response = await fetch("http://localhost:8000/directory", {
        method: "GET",
        headers: headers
    });
    const elements = await response.json();
    for (let elem of elements) {
        let option = document.createElement("option");
        option.text = elem;
        option.value = elem;
        fileSelect.appendChild(option);
    }
}

window.onload = getFilesFromServer;
