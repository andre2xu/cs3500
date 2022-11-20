import {
    CALENDAR,
    CLOCK,
    ADD_FORM,
    EDIT_FORM
} from './data.js';

import {
    updateTemporalMetrics,
    loadServerMetrics,
    activateServer,
    deactivateServer,
    restartServer,
    loadActivePlots
} from './helpers.js';



let selectedServer = document.querySelector('[data-server-num="0"]');



window.addEventListener('load', (e) => {
    updateTemporalMetrics(CALENDAR, CLOCK);
    loadActivePlots();

    setInterval(() => {
        updateTemporalMetrics(CALENDAR, CLOCK);
    }, 1000);



    document.getElementById('serverList').addEventListener('click', (e) => {
        let serverListing = e.target;

        if (serverListing.parentElement.hasAttribute('data-server-num')) {
            serverListing = serverListing.parentElement;
        }

        if (serverListing.hasAttribute('data-server-num') && serverListing !== selectedServer) {
            serverListing.classList.add('selected');
            selectedServer.classList.remove('selected');

            selectedServer = serverListing;

            loadServerMetrics(selectedServer.getAttribute('data-server-num'));
        }
    });


    document.getElementById('serverButtons').addEventListener('click', (e) => {
        const BUTTON = e.target.innerText;
        const SERVER_NUM = selectedServer.getAttribute('data-server-num');

        switch (BUTTON) {
            case 'Activate':
                activateServer(SERVER_NUM, selectedServer);
                break;
            case 'Deactivate':
                deactivateServer(SERVER_NUM, selectedServer);
                break;
            case 'Restart':
                restartServer(SERVER_NUM, selectedServer);
                break;
        }
    });



    document.getElementById('interfaceButtons').addEventListener('click', (e) => {
        const BUTTON = e.target.innerText;

        switch (BUTTON) {
            case 'Add':
                EDIT_FORM.classList.add('hidden');
                ADD_FORM.classList.remove('hidden');
                break;
            case 'Edit':
                ADD_FORM.classList.add('hidden');
                EDIT_FORM.classList.remove('hidden');
                break;
            case 'Delete':
                break;
        }
    });
})