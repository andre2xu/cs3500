import {
    CALENDAR,
    CLOCK,
    ADD_FORM,
    EDIT_FORM,
    FARM_MAP
} from './data.js';

import {
    updateTemporalMetrics,
    updateHarvestCountdown,
    loadServerMetrics,
    activateServer,
    deactivateServer,
    restartServer,
    submitForm,
    loadActivePlots,
    loadPlotsReadyForHarvesting,
    deleteGrowthRequirements,
    loadGrowthRequirements,
    loadSensorData,
    updateSwitches,
    sendSwitchDataToBackend,
    activateFertilizer,
    deactivateMapPlot
} from './helpers.js';



let selectedServer = document.querySelector('[data-server-num="0"]');
let selectedPlot = document.querySelector('[data-plot-num="0"]');



window.addEventListener('load', () => {
    updateTemporalMetrics(CALENDAR, CLOCK);

    const PLOT_NUM = selectedPlot.firstElementChild.innerText.split('#')[1];
    loadActivePlots();
    loadPlotsReadyForHarvesting();
    loadGrowthRequirements(PLOT_NUM);
    loadSensorData(PLOT_NUM);

    setInterval(() => {
        updateTemporalMetrics(CALENDAR, CLOCK);
        updateHarvestCountdown();

        loadSensorData(selectedPlot.firstElementChild.innerText.split('#')[1]);
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
    document.getElementById('addCropSubmitButton').addEventListener('click', (e) => {
        e.preventDefault();

        submitForm(ADD_FORM, '/api/addCrop', true);

        const SELECTED_PLOT_NUM = selectedPlot.firstElementChild.innerText.split('#')[1];

        // only loads growth requirements if it the newly added requirements are for the currently selected plot
        if (ADD_FORM.querySelector('#addPlotNum').value === SELECTED_PLOT_NUM) {
            loadGrowthRequirements(SELECTED_PLOT_NUM);
            loadSensorData(SELECTED_PLOT_NUM);
            updateHarvestCountdown();
        }
    });

    document.getElementById('editCropSubmitButton').addEventListener('click', (e) => {
        e.preventDefault();

        submitForm(EDIT_FORM, '/api/editCrop', false);

        const SELECTED_PLOT_NUM = selectedPlot.firstElementChild.innerText.split('#')[1];

        // only loads growth requirements if it the updated requirements are for the currently selected plot
        if (EDIT_FORM.querySelector('#editPlotNum').value === SELECTED_PLOT_NUM) {
            loadGrowthRequirements(SELECTED_PLOT_NUM);
            updateHarvestCountdown();
        }
    });

    document.getElementById('interfaceButtons').addEventListener('click', (e) => {
        const BUTTON = e.target.innerText;
        const SELECTED_PLOT_NUM = selectedPlot.firstElementChild.innerText.split('#')[1]; 

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
                const PLOT = selectedPlot.lastElementChild;

                if (PLOT.classList.contains('green')) {
                    deleteGrowthRequirements(SELECTED_PLOT_NUM);
                    loadSensorData(SELECTED_PLOT_NUM);
                    deactivateMapPlot(SELECTED_PLOT_NUM);

                    window.harvestDate = null;
                    updateHarvestCountdown();
                }
                else if (PLOT.classList.contains('orange')) {
                    deleteGrowthRequirements(SELECTED_PLOT_NUM);
                    deactivateMapPlot(SELECTED_PLOT_NUM);
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

            const SELECTED_PLOT_NUM = selectedPlot.firstElementChild.innerText.split('#')[1];

            document.getElementById('addPlotNum').value = SELECTED_PLOT_NUM;
            document.getElementById('editPlotNum').value = SELECTED_PLOT_NUM;

            loadGrowthRequirements(SELECTED_PLOT_NUM);
            updateHarvestCountdown();
            loadSensorData(SELECTED_PLOT_NUM);
            updateSwitches(SELECTED_PLOT_NUM);
        }
    });



    // SWITCHES
    document.getElementById('inputSwitches').addEventListener('click', (e) => {
        const ELEMENT_CLICKED = e.target;

        if (ELEMENT_CLICKED.classList.contains('switch')) {
            const SWITCH = ELEMENT_CLICKED.parentElement;
            const INPUT_ELEMENTS = SWITCH.querySelectorAll('input');

            switch (SWITCH.id) {
                case 'sprinklers':
                    sendSwitchDataToBackend({
                        component: 'sprinkler',
                        plotNum: INPUT_ELEMENTS[0].value,
                        activationDuration: INPUT_ELEMENTS[1].value,
                        pH: INPUT_ELEMENTS[2].value
                    });
                    break;
                case 'fertilizers':
                    activateFertilizer(INPUT_ELEMENTS[1].value);
                    break;
                case 'temperature':
                    sendSwitchDataToBackend({
                        component: 'temperatureModifier',
                        plotNum: INPUT_ELEMENTS[0].value,
                        activationDuration: INPUT_ELEMENTS[1].value,
                        temperature: INPUT_ELEMENTS[2].value
                    });
                    break;
                case 'lighting':
                    sendSwitchDataToBackend({
                        component: 'lightingModifier',
                        plotNum: INPUT_ELEMENTS[0].value,
                        activationDuration: INPUT_ELEMENTS[1].value
                    });
                    break;
                case 'co2':
                    sendSwitchDataToBackend({
                        component: 'co2Modifier',
                        plotNum: INPUT_ELEMENTS[0].value,
                        activationDuration: INPUT_ELEMENTS[1].value,
                        ppm: INPUT_ELEMENTS[2].value
                    });
                    break;
            }
        }
    });



    // MAP
    FARM_MAP.addEventListener('click', (e) => {
        const ELEMENT_CLICKED = e.target;

        if (ELEMENT_CLICKED.hasAttribute('data-map-plot')) {
            const PLOT_NUM = ELEMENT_CLICKED.getAttribute('data-map-plot');

            if (PLOT_NUM !== selectedPlot.getAttribute('data-plot-num')) {
                const PLOT_LISTING_TO_SELECT = document.querySelector(`[data-plot-num="${PLOT_NUM}"]`);

                PLOT_LISTING_TO_SELECT.classList.add('selected');
                selectedPlot.classList.remove('selected');

                selectedPlot = PLOT_LISTING_TO_SELECT;

                document.getElementById('addPlotNum').value = PLOT_NUM;
                document.getElementById('editPlotNum').value = PLOT_NUM;

                loadGrowthRequirements(PLOT_NUM);
                updateHarvestCountdown();
                loadSensorData(PLOT_NUM);
                updateSwitches(PLOT_NUM);
            }
        }
    });
});