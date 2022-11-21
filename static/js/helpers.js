import {
    SERVER_METRICS,
    SERVER_METRICS_LIST,
    PLOT_GR_DAYS,
    PLOT_GR_SEED_TEMPERATURE,
    PLOT_GR_CROP_TEMPERATURE,
    PLOT_GR_PH,
    PLOT_GR_CO2_CONCENTRATION,
    PLOT_GR_LIGHT_EXPOSURE,
    PLOT_GR_WATER_DEPTH,
    PLOT_GR_WATERING_INTERVAL
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
export function submitForm(form, url, getResponse) {
    const XHR = new XMLHttpRequest();
    XHR.open('POST', url, false);

    if (getResponse) {
        XHR.onreadystatechange = function () {
            const RESPONSE = XHR.responseText;

            if (RESPONSE.length === 1) {
                document.querySelector(`[data-plot-num="${RESPONSE}"]`).lastElementChild.classList.replace('red', 'green');
            }
        };
    }

    XHR.send(new FormData(form));

    form.classList.add('hidden');
};

export function loadActivePlots() {
    const XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function () {
        const RESPONSE = XHR.responseText;
        const NUMBER_OF_PLOTS = RESPONSE.length;

        if (NUMBER_OF_PLOTS > 0) {
            for (let i=0; i < NUMBER_OF_PLOTS; i++) {
                document.querySelector(`[data-plot-num="${RESPONSE[i]}"]`).lastElementChild.classList.replace('red', 'green');
            }
        }
    }
    XHR.open('GET', '/db/activePlots', true);
    XHR.send(null);
};

export function deleteGrowthRequirements(plotNum) {
    const XHR = new XMLHttpRequest();
    XHR.open('GET', `/api/deleteCrop/${plotNum}`, false);
    XHR.send(null);

    document.querySelector(`[data-plot-num="${plotNum}"]`).lastElementChild.classList.replace('green', 'red');
};

export function loadGrowthRequirements(plotNum) {
    const XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function () {
        const RESPONSE = XHR.responseText;

        PLOT_GR_DAYS.innerText = 'Days:';
        PLOT_GR_SEED_TEMPERATURE.innerText = 'Seed temperature (°C):';
        PLOT_GR_CROP_TEMPERATURE.innerText = 'Crop temperature (°C):';
        PLOT_GR_PH.innerText = 'pH:';
        PLOT_GR_CO2_CONCENTRATION.innerHTML = 'CO<sub>2</sub> concentration (ppm):';
        PLOT_GR_LIGHT_EXPOSURE.innerText = 'Light exposure duration (hrs):';
        PLOT_GR_WATER_DEPTH.innerText = 'Water supply depth (in):';
        PLOT_GR_WATERING_INTERVAL.innerText = 'Watering interval (hrs):';

        if (RESPONSE.length > 0) {
            const GROWTH_REQUIREMENTS = JSON.parse(RESPONSE);

            PLOT_GR_DAYS.innerText += ` ${GROWTH_REQUIREMENTS['days']}`;

            PLOT_GR_SEED_TEMPERATURE.innerText += ` ${GROWTH_REQUIREMENTS['seedTemperature']}`;

            PLOT_GR_CROP_TEMPERATURE.innerText += ` ${GROWTH_REQUIREMENTS['cropTemperature']}`;

            PLOT_GR_PH.innerText += ` ${GROWTH_REQUIREMENTS['pH']}`;

            PLOT_GR_CO2_CONCENTRATION.innerHTML += ` ${GROWTH_REQUIREMENTS['co2Concentration']}`;

            PLOT_GR_LIGHT_EXPOSURE.innerText += ` ${GROWTH_REQUIREMENTS['lightExposureDuration']}`;

            PLOT_GR_WATER_DEPTH.innerText += ` ${GROWTH_REQUIREMENTS['waterDepth']}`;

            PLOT_GR_WATERING_INTERVAL.innerText += ` ${GROWTH_REQUIREMENTS['wateringInterval']}`;
        }
    }
    XHR.open('GET', `/db/growthRequirements/${plotNum}`, true);
    XHR.send(null);
};

export function loadSensorData(plotNum) {
    const XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function () {
        const RESPONSE = XHR.responseText;
    }
    XHR.open('GET', `/db/sensorData/${plotNum}`, true);
    XHR.send(null);
};