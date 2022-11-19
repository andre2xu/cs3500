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
]