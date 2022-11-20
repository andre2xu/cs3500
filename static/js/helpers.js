import {
    SERVER_METRICS,
    SERVER_METRICS_LIST
} from './data.js';



export function updateTemporalMetrics(calendar, clock) {
    const DATE = new Date();

    let day = `${DATE.getDate()}`;
    let month = `${DATE.getMonth() + 1}`;
    let year = `${DATE.getFullYear()}`;
    let hrs = `${DATE.getUTCHours()}`;
    let mins = `${DATE.getUTCMinutes()}`;

    if (day.length === 1) {
        day = '0' + day;
    }
    if (month.length === 1) {
        month = '0' + month;
    }
    if (hrs.length === 1) {
        hrs = '0' + hrs;
    }
    if (mins.length === 1) {
        mins = '0' + mins;
    }

    calendar.innerText = `Date: ${day}/${month}/${year}`;

    clock.innerText = `Time: ${hrs}:${mins}`;
};



// SERVER API
export function loadServerMetrics(serverNum) {
    const METRICS = SERVER_METRICS[serverNum];

    SERVER_METRICS_LIST[0].innerText = `Variable: ${METRICS['variable']}`;
    SERVER_METRICS_LIST[1].innerText = `Status: ${METRICS['status']}`;
};

export function activateServer(serverNum, selectedServer) {
    SERVER_METRICS[serverNum]['status'] = 'ONLINE';

    selectedServer.lastElementChild.classList.replace('red', 'green');

    loadServerMetrics(serverNum);
};

export function deactivateServer(serverNum, selectedServer) {
    SERVER_METRICS[serverNum]['status'] = 'OFFLINE';

    selectedServer.lastElementChild.classList.replace('green', 'red');

    loadServerMetrics(serverNum);
};

export function restartServer(serverNum, selectedServer) {
    SERVER_METRICS[serverNum]['status'] = 'RESTARTING';

    selectedServer.lastElementChild.classList.replace('green', 'red');
    loadServerMetrics(serverNum);

    setTimeout(() => {
        selectedServer.lastElementChild.classList.replace('red', 'green');
        SERVER_METRICS[serverNum]['status'] = 'ONLINE';

        if (selectedServer.classList.contains('selected')) {
            loadServerMetrics(serverNum);
        }
    }, 3000);
};



// PLOT API
export function loadActivePlots() {
    const XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function () {
        let response = XHR.responseText;

        if (response.length > 0) {
            console.log(response);
        }
    }
    XHR.open('GET', '/db/activePlots', true);
    XHR.send(null);
};