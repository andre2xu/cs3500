const CALENDAR = document.getElementById('dynamicCalendar');
const CLOCK = document.getElementById('dynamicClock');

setInterval(() => {
    const DATE = new Date();

    CALENDAR.innerText = `Date: ${DATE.getUTCDay()}/${DATE.getUTCMonth()}/${DATE.getUTCFullYear()}`;

    CLOCK.innerText = `Time: ${DATE.getUTCHours()}:${DATE.getUTCMinutes()}`;
}, 1000)