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
}