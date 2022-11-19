import {
    updateTemporalMetrics
} from './helpers.js';



const CALENDAR = document.getElementById('dynamicCalendar');
const CLOCK = document.getElementById('dynamicClock');



window.addEventListener('load', () => {
    updateTemporalMetrics(CALENDAR, CLOCK);

    setInterval(() => {
        updateTemporalMetrics(CALENDAR, CLOCK);
    }, 1000);
})