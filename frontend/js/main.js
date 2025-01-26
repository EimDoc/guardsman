
async function startDynamicAnalysis() {
    let file = document.getElementById("file-selection");
    file = file.options[file.selectedIndex].value;

    let systemType = document.getElementById("os-selection");
    systemType = systemType.options[systemType.selectedIndex].text;

    if (!file) {
        alert("Выберите файл для проверки!");
    } else if (systemType === "Выберите ОС") {
        alert("Выберите ОС, на которой будет проверяться файл");
    } else {
        const data = {path_to_file: file}
        await fetch(
            "http://localhost:8000/dynamic_analyze", {
                method: "POST",
                headers: {'Content-Type': 'application/json;charset=utf-8'},
                body: JSON.stringify(data)
            });
        await listenLogsFromServer();
        console.log("do something...");
        console.log(systemType);
        console.log(file);
    }
}

async function getFilesFromServer() {
    const fileSelect = document.getElementById("file-selection");

    const headers = new Headers();


    const response = await fetch(
        "http://localhost:8000/directory", {
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


async function startStaticAnalysis() {
    let file = document.getElementById("file-selection");
    file = file.options[file.selectedIndex].value;

    if (!file) {
        alert("Выберите файл для проверки!");
    } else {
        const output = document.getElementById("output");
        output.innerText = '';
        const p = document.createElement('p');
        p.textContent = "Статический анализ файла начат...";
        output.appendChild(p);

        const data = {path_to_file: file}
        const response = await fetch(
            "http://localhost:8000/static_analyze", {
                method: "POST",
                headers: {'Content-Type': 'application/json;charset=utf-8'},
                body: JSON.stringify(data)
            });

        const text = await response.text()

        p.textContent = text;
        output.appendChild(p);
    }
}


async function listenLogsFromServer() {
    const output = document.getElementById("output");
    const eventSource = new EventSource("http://localhost:8000/logs_stream");

    eventSource.onopen = () => {
        console.log('EventSource connected')
        output.innerText = '';
    }

    eventSource.onmessage = (event) => {
        const p = document.createElement('p');
        p.textContent = event.data;
        output.appendChild(p);
    };

    eventSource.onerror = () => {
        console.error('Connection Closed');
        eventSource.close();
    };
}

async function doWhenPageLoad() {
    await getFilesFromServer();
}

window.onload = doWhenPageLoad;
