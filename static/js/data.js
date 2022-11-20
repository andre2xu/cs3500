export const CALENDAR = document.getElementById('dynamicCalendar');
export const CLOCK = document.getElementById('dynamicClock');
export const ADD_FORM = document.getElementById('addCrop');
export const EDIT_FORM = document.getElementById('editCrop');



export const SERVER_METRICS_LIST = document.getElementById('serverMetrics').children;

export const SERVER_METRICS = [
    {
        variable: 'Light levels',
        status: 'ONLINE'
    },
    {
        variable: 'Soil temperature',
        status: 'ONLINE'
    },
    {
        variable: 'CO2 concentration',
        status: 'ONLINE'
    },
    {
        variable: 'Soil pH',
        status: 'ONLINE'
    },
    {
        variable: 'Soil moisture',
        status: 'ONLINE'
    }
];



export const PLOT_METRICS_LIST = document.getElementById('cropMetrics');

export const PLOT_LIGHT_LEVELS = PLOT_METRICS_LIST.querySelector('[data-sd-light]');
export const PLOT_SOIL_TEMPERATURE = PLOT_METRICS_LIST.querySelector('[data-sd-soil-temperature]');
export const PLOT_CO2_CONCENTRATION = PLOT_METRICS_LIST.querySelector('[data-sd-co2-concentration]');
export const PLOT_SOIL_PH = PLOT_METRICS_LIST.querySelector('[data-sd-soil-pH]');
export const PLOT_SOIL_MOISTURE = PLOT_METRICS_LIST.querySelector('[data-sd-soil-moisture]');

export const PLOT_SPRINKLER_STATUS = PLOT_METRICS_LIST.querySelector('[data-sprinkler-status]');
export const PLOT_FERTILIZER_STATUS = PLOT_METRICS_LIST.querySelector('[data-fertilizer-status]');

export const PLOT_TEMPERATURE_MODIFIER_STATUS = PLOT_METRICS_LIST.querySelector('[data-temperature-modifier-status]');
export const PLOT_LIGHTING_MODIFIER_STATUS = PLOT_METRICS_LIST.querySelector('[data-lighting-modifier-status]');
export const PLOT_CO2_MODIFIER_STATUS = PLOT_METRICS_LIST.querySelector('[data-co2-modifier-status]');

export const PLOT_GR_DAYS = PLOT_METRICS_LIST.querySelector('[data-gr-days]');
export const PLOT_GR_SEED_TEMPERATURE = PLOT_METRICS_LIST.querySelector('[data-gr-seed-temperature]');
export const PLOT_GR_CROP_TEMPERATURE = PLOT_METRICS_LIST.querySelector('[data-gr-crop-temperature]');
export const PLOT_GR_PH = PLOT_METRICS_LIST.querySelector('[data-gr-pH]');
export const PLOT_GR_CO2_CONCENTRATION = PLOT_METRICS_LIST.querySelector('[data-gr-co2-concentration]');
export const PLOT_GR_LIGHT_EXPOSURE = PLOT_METRICS_LIST.querySelector('[data-gr-light-exposure]');
export const PLOT_GR_WATER_DEPTH = PLOT_METRICS_LIST.querySelector('[data-gr-water-depth]');
export const PLOT_GR_WATERING_INTERVAL = PLOT_METRICS_LIST.querySelector('[data-gr-watering-interval]');