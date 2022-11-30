import "https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js";

import {
    FARM_MAP,
    HARVEST_COUNTDOWN,
    SERVER_METRICS,
    SERVER_METRICS_LIST,
    SWITCH_TARGETS,
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
    PLOT_SOIL_MOISTURE,
    SENSOR_DATA_DISPLAY_STATUS,
    PLOT_SPRINKLER_STATUS,
    PLOT_FERTILIZER_STATUS,
    PLOT_TEMPERATURE_MODIFIER_STATUS,
    PLOT_LIGHTING_MODIFIER_STATUS,
    PLOT_CO2_MODIFIER_STATUS
} from './data.js';



const SOCKET = io();
SOCKET.connect('http://127.0.0.1:5000/');

SOCKET.on('message', (msg) => {
    if (msg.constructor === Object) {
        if (msg['sprinkler'] !== undefined && PLOT_SPRINKLER_STATUS.innerText.includes('OFF')) {
            activateSprinkler(`${msg['sprinkler']}`, true);
        }
        else if (msg['tempModifier'] !== undefined && PLOT_TEMPERATURE_MODIFIER_STATUS.innerText.includes('OFF')) {
            activateTempModifier(`${msg['tempModifier']}`);
        }
        else if (msg['lightModifier'] !== undefined && PLOT_LIGHTING_MODIFIER_STATUS.innerText.includes('OFF')) {
            activateLightModifier(`${msg['lightModifier']}`);
        }
        else if (msg['co2Modifier'] !== undefined && PLOT_CO2_MODIFIER_STATUS.innerText.includes('OFF')) {
            activateCO2Modifier(`${msg['co2Modifier']}`);
        }
    }
});



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
        let daysLeft = Math.round(Math.abs(window.harvestDate - CURRENT_DATE) / 8.64e+7);
        let hrsLeft = 24 - CURRENT_DATE.getHours();
        let minsLeft = 60 - CURRENT_DATE.getMinutes();

        if (daysLeft < 0) {
            daysLeft = '00';
        }
        else if (daysLeft < 10) {
            daysLeft = `0${daysLeft}`;
        }

        if (hrsLeft < 0) {
            hrsLeft = '00';
        }
        else if (hrsLeft < 10) {
            hrsLeft = `0${hrsLeft}`;
        }

        if (minsLeft < 0) {
            minsLeft = '00';
        }
        else if (minsLeft < 10) {
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

export function toggleSensorVariableCollection(serverNum) {
    switch (serverNum) {
        case '0':
            SENSOR_DATA_DISPLAY_STATUS['lightLevels'] = (SENSOR_DATA_DISPLAY_STATUS['lightLevels'] ? false : true); 
            break;
        case '1':
            SENSOR_DATA_DISPLAY_STATUS['soilTemp'] = (SENSOR_DATA_DISPLAY_STATUS['soilTemp'] ? false : true); 
            break;
        case '2':
            SENSOR_DATA_DISPLAY_STATUS['co2'] = (SENSOR_DATA_DISPLAY_STATUS['co2'] ? false : true); 
            break;
        case '3':
            SENSOR_DATA_DISPLAY_STATUS['pH'] = (SENSOR_DATA_DISPLAY_STATUS['pH'] ? false : true); 
            break;
        case '4':
            SENSOR_DATA_DISPLAY_STATUS['soilMoisture'] = (SENSOR_DATA_DISPLAY_STATUS['soilMoisture'] ? false : true); 
            break;
    }
};

export function activateServer(serverNum, selectedServer) {
    SERVER_METRICS[serverNum]['status'] = 'ONLINE';

    selectedServer.lastElementChild.classList.replace('red', 'green');

    toggleSensorVariableCollection(serverNum);
    loadServerMetrics(serverNum);
};

export function deactivateServer(serverNum, selectedServer) {
    SERVER_METRICS[serverNum]['status'] = 'OFFLINE';

    selectedServer.lastElementChild.classList.replace('green', 'red');

    toggleSensorVariableCollection(serverNum);
    loadServerMetrics(serverNum);
};

export function restartServer(serverNum, selectedServer) {
    SERVER_METRICS[serverNum]['status'] = 'RESTARTING';

    selectedServer.lastElementChild.classList.replace('green', 'red');

    toggleSensorVariableCollection(serverNum);
    loadServerMetrics(serverNum);

    setTimeout(() => {
        selectedServer.lastElementChild.classList.replace('red', 'green');
        SERVER_METRICS[serverNum]['status'] = 'ONLINE';

        toggleSensorVariableCollection(serverNum);

        if (selectedServer.classList.contains('selected')) {
            loadServerMetrics(serverNum);
        }
    }, 10000);
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

                activateMapPlot(RESPONSE);
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
                const PLOT_NUM = RESPONSE[i];

                document.querySelector(`[data-plot-num="${PLOT_NUM}"]`).lastElementChild.classList.replace('red', 'green');

                activateMapPlot(PLOT_NUM);
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

    PLOT_GR_DAYS.innerText = 'Days:';
    PLOT_GR_SEED_TEMPERATURE.innerText = 'Seed temperature (°C):';
    PLOT_GR_CROP_TEMPERATURE.innerText = 'Crop temperature (°C):';
    PLOT_GR_PH.innerText = 'pH:'
    PLOT_GR_CO2_CONCENTRATION.innerHTML = 'CO<sub>2</sub> concentration (ppm):';
    PLOT_GR_LIGHT_EXPOSURE.innerText = 'Light exposure duration (hrs):';
    PLOT_GR_WATER_DEPTH.innerText = 'Water supply depth (in):';
    PLOT_GR_WATERING_INTERVAL.innerText = 'Watering interval (hrs):';

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

            if (SENSOR_DATA_DISPLAY_STATUS['lightLevels'] === true) {
                PLOT_LIGHT_LEVELS.innerText += ` ${SENSOR_DATA['lighting']}`;
            }
            if (SENSOR_DATA_DISPLAY_STATUS['soilTemp'] === true) {
                PLOT_SOIL_TEMPERATURE.innerText += ` ${SENSOR_DATA['soilTemp']}`;
            }
            if (SENSOR_DATA_DISPLAY_STATUS['co2'] === true) {
                PLOT_CO2_CONCENTRATION.innerText += ` ${SENSOR_DATA['co2']}`;
            }
            if (SENSOR_DATA_DISPLAY_STATUS['pH'] === true) {
                PLOT_SOIL_PH.innerText += ` ${SENSOR_DATA['pH']}`;
            }
            if (SENSOR_DATA_DISPLAY_STATUS['soilMoisture'] === true) {
                PLOT_SOIL_MOISTURE.innerText += ` ${SENSOR_DATA['moisture']}`;
            }
        }
    }
    XHR.open('GET', `/api/sensorData/${plotNum}`, true);
    XHR.send(null);
};



// SWITCHES
export function updateSwitches(newPlotNum) {
    const NUM_OF_TARGETS = SWITCH_TARGETS.length;

    for (let i=0; i < NUM_OF_TARGETS; i++) {
        SWITCH_TARGETS[i].value = newPlotNum;
    }
};

export function sendSwitchDataToBackend(data) {
    const XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function () {
        const COMPONENTS_TO_TURN_ON = XHR.responseText;
        const NUM_OF_COMPONENTS = COMPONENTS_TO_TURN_ON.length;

        if (NUM_OF_COMPONENTS > 0) {
            const ACTIVATION_DURATION = data['activationDuration'];

            for (let i=0; i < NUM_OF_COMPONENTS; i++) {
                const COMPONENT_INITIAL_LETTER = COMPONENTS_TO_TURN_ON[i];

                switch (COMPONENT_INITIAL_LETTER) {
                    case 's':
                        activateSprinkler(ACTIVATION_DURATION);
                        break;
                    case 't':
                        activateTempModifier(ACTIVATION_DURATION);
                    case 'l':
                        activateLightModifier(ACTIVATION_DURATION);
                    case 'c':
                        activateCO2Modifier(ACTIVATION_DURATION);
                }
            }
        }
    }
    XHR.open('POST', '/api/switchHandler', true);
    XHR.setRequestHeader("Content-Type", "application/json");
    XHR.send(JSON.stringify(data));
};

export function activateSprinkler(duration, for_pH=false) {
    duration = parseInt(duration);

    PLOT_SPRINKLER_STATUS.innerText = 'Sprinkler: ON';

    if (for_pH === false) {
        let soilMoisture = parseFloat(PLOT_SOIL_MOISTURE.innerText.split(': ')[1]);

        for (let i=0; i < duration; i++) {
            const NEW_MOISTURE = soilMoisture + 12.5;

            if (NEW_MOISTURE < 100.0) {
                soilMoisture = NEW_MOISTURE;
            }
            else {
                duration = i; // real duration of sprinkler activation
            }
        }
    }

    setTimeout(() => {
        PLOT_SPRINKLER_STATUS.innerText = 'Sprinkler: OFF';
    }, duration * 1000);
};

export function activateFertilizer(duration) {
    PLOT_FERTILIZER_STATUS.innerText = 'Fertilizer: ON';

    setTimeout(() => {
        PLOT_FERTILIZER_STATUS.innerText = 'Fertilizer: OFF';
    }, parseInt(duration) * 1000);
};

export function activateTempModifier(duration) {
    duration = parseInt(duration);

    PLOT_TEMPERATURE_MODIFIER_STATUS.innerText = 'Temperature Modifier: ON';

    setTimeout(() => {
        PLOT_TEMPERATURE_MODIFIER_STATUS.innerText = 'Temperature Modifier: OFF';
    }, duration * 1000);
};

export function activateLightModifier(duration) {
    duration = parseInt(duration);

    PLOT_LIGHTING_MODIFIER_STATUS.innerText = 'Lighting Modifier: ON';

    setTimeout(() => {
        PLOT_LIGHTING_MODIFIER_STATUS.innerText = 'Lighting Modifier: OFF';
    }, duration * 1000);
};

export function activateCO2Modifier(duration) {
    duration = parseInt(duration);

    PLOT_CO2_MODIFIER_STATUS.innerHTML = 'CO<sub>2</sub> Modifier: ON';

    setTimeout(() => {
        PLOT_CO2_MODIFIER_STATUS.innerHTML = 'CO<sub>2</sub> Modifier: OFF';
    }, duration * 1000);
};




// MAP
export function activateMapPlot(plotNum) {
    FARM_MAP.querySelector(`[data-map-plot="${plotNum}"]`).classList.add('active');
};

export function deactivateMapPlot(plotNum) {
    FARM_MAP.querySelector(`[data-map-plot="${plotNum}"]`).classList.remove('active');
};
