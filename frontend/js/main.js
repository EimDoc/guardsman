
async function startDynamicAnalyze() {
    let file = document.getElementById("file-selection");
    file = file.options[file.selectedIndex].value;

    let systemType = document.getElementById("os-selection");
    systemType = systemType.options[systemType.selectedIndex].text;

    if (!file) {
        alert("Выберите файл для проверки!");
    } else if (systemType === "Выберите ОС") {
        alert("Выберите ОС, на которой будет проверяться файл");
    } else {
        await listenLogsFromServer();
        console.log("do something...");
        console.log(systemType);
        console.log(file);
    }
}

async function getFilesFromServer() {
    const fileSelect = document.getElementById("file-selection");

    const headers = new Headers();


    const response = await fetch("http://10.10.16.150:8000/directory", {
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


async function listenLogsFromServer() {
    const output = document.getElementById("output");
    const eventSource = new EventSource("http://10.10.16.150:8000/logs_stream");

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
