export function updateTemporalMetrics(calendar, clock) {
    const DATE = new Date();

    calendar.innerText = `Date: ${DATE.getDate()}/${DATE.getMonth() + 1}/${DATE.getFullYear()}`;

    clock.innerText = `Time: ${DATE.getUTCHours()}:${DATE.getUTCMinutes()}`;
}