import {
    HARVEST_COUNTDOWN,
    SERVER_METRICS,
    SERVER_METRICS_LIST,
    PLOT_GR_DAYS,
    PLOT_GR_SEED_TEMPERATURE,
    PLOT_GR_CROP_TEMPERATURE,
    PLOT_GR_PH,
    PLOT_GR_CO2_CONCENTRATION,
    PLOT_GR_LIGHT_EXPOSURE,
    PLOT_GR_WATER_DEPTH,
    PLOT_GR_WATERING_INTERVAL,
    PLOT_LIGHT_LEVELS,
    PLOT_SOIL_TEMPERATURE,
    PLOT_CO2_CONCENTRATION,
    PLOT_SOIL_PH,
    PLOT_SOIL_MOISTURE
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

export function updateHarvestCountdown() {
    if (window.harvestDate !== null) {
        const CURRENT_DATE = new Date();
        let daysLeft = window.harvestDate.getDate() - CURRENT_DATE.getDate();
        let hrsLeft = 24 - CURRENT_DATE.getHours();
        let minsLeft = 60 - CURRENT_DATE.getMinutes();

        if (daysLeft < 10) {
            daysLeft = `0${daysLeft}`;
        }
        if (hrsLeft < 10) {
            hrsLeft = `0${hrsLeft}`;
        }
        if (minsLeft < 10) {
            minsLeft = `0${minsLeft}`;
        }

        HARVEST_COUNTDOWN.innerText = `Harvest due in: ${daysLeft}d:${hrsLeft}h:${minsLeft}m`;
    }
    else {
        HARVEST_COUNTDOWN.innerText = 'Harvest due in: 00d:00h:00m';
    }
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

        let days = 'Days:';
        let seedTemp = 'Seed temperature (°C):';
        let cropTemp = 'Crop temperature (°C):';
        let pH = 'pH:';
        let co2 = 'CO<sub>2</sub> concentration (ppm):';
        let lightExposureDuration = 'Light exposure duration (hrs):';
        let waterDepth = 'Water supply depth (in):';
        let wateringInterval = 'Watering interval (hrs):';

        window.harvestDate = null;

        if (RESPONSE.length > 0) {
            const GROWTH_REQUIREMENTS = JSON.parse(RESPONSE);

            window.harvestDate = new Date(GROWTH_REQUIREMENTS['harvestDate']);

            days += ` ${GROWTH_REQUIREMENTS['days']}`;

            seedTemp += ` ${GROWTH_REQUIREMENTS['seedTemperature']}`;

            cropTemp += ` ${GROWTH_REQUIREMENTS['cropTemperature']}`;

            pH += ` ${GROWTH_REQUIREMENTS['pH']}`;

            co2 += ` ${GROWTH_REQUIREMENTS['co2Concentration']}`;

            lightExposureDuration += ` ${GROWTH_REQUIREMENTS['lightExposureDuration']}`;

            waterDepth += ` ${GROWTH_REQUIREMENTS['waterDepth']}`;

            wateringInterval += ` ${GROWTH_REQUIREMENTS['wateringInterval']}`;
        }

        PLOT_GR_DAYS.innerText = days;
        PLOT_GR_SEED_TEMPERATURE.innerText = seedTemp;
        PLOT_GR_CROP_TEMPERATURE.innerText = cropTemp;
        PLOT_GR_PH.innerText = pH;
        PLOT_GR_CO2_CONCENTRATION.innerHTML = co2;
        PLOT_GR_LIGHT_EXPOSURE.innerText = lightExposureDuration;
        PLOT_GR_WATER_DEPTH.innerText = waterDepth;
        PLOT_GR_WATERING_INTERVAL.innerText = wateringInterval;
    }
    XHR.open('GET', `/db/growthRequirements/${plotNum}`, true);
    XHR.send(null);
};

export function loadSensorData(plotNum) {
    const XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function () {
        const RESPONSE = XHR.responseText;

        PLOT_LIGHT_LEVELS.innerText = 'Light levels (lux):';
        PLOT_SOIL_TEMPERATURE.innerText = 'Soil temperature (°C):';
        PLOT_CO2_CONCENTRATION.innerHTML = 'CO<sub>2</sub> concentration (ppm):';
        PLOT_SOIL_PH.innerText = 'Soil pH:';
        PLOT_SOIL_MOISTURE.innerText = 'Soil moisture (%):';

        if (RESPONSE.length > 0) {
            const SENSOR_DATA = JSON.parse(RESPONSE);

            PLOT_LIGHT_LEVELS.innerText += ` ${SENSOR_DATA['lighting']}`;
            PLOT_SOIL_TEMPERATURE.innerText += ` ${SENSOR_DATA['soilTemp']}`;
            PLOT_CO2_CONCENTRATION.innerText += ` ${SENSOR_DATA['co2']}`;
            PLOT_SOIL_PH.innerText += ` ${SENSOR_DATA['pH']}`;
            PLOT_SOIL_MOISTURE.innerText += ` ${SENSOR_DATA['moisture']}`;
        }
    }
    XHR.open('GET', `/api/sensorData/${plotNum}`, true);
    XHR.send(null);
};