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
    loadActivePlots,
    deleteGrowthRequirements,
    loadGrowthRequirements
} from './helpers.js';



let selectedServer = document.querySelector('[data-server-num="0"]');
let selectedPlot = document.querySelector('[data-plot-num="0"]');



window.addEventListener('load', () => {
    updateTemporalMetrics(CALENDAR, CLOCK);

    loadActivePlots();
    loadGrowthRequirements(selectedPlot.firstElementChild.innerText.split('#')[1]);

    setInterval(() => {
        updateTemporalMetrics(CALENDAR, CLOCK);
    }, 1000);



    // SERVER LIST
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



    // PLOT LIST
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
                if (selectedPlot.lastElementChild.classList.contains('green')) {
                    deleteGrowthRequirements(selectedPlot.firstElementChild.innerText.split('#')[1]);
                }

                break;
        }
    });

    document.getElementById('plotList').addEventListener('click', (e) => {
        let plotListing = e.target;

        if (plotListing.parentElement.hasAttribute('data-plot-num')) {
            plotListing = plotListing.parentElement;
        }

        if (plotListing.hasAttribute('data-plot-num') && plotListing !== selectedPlot) {
            plotListing.classList.add('selected');
            selectedPlot.classList.remove('selected');

            selectedPlot = plotListing;

            loadGrowthRequirements(selectedPlot.firstElementChild.innerText.split('#')[1]);
        }
    });
})