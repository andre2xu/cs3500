# CURRENTLY WORKING PARTS OF THE UI:
- Date and time metrics under the map (black box)
- Server list indicator lights
- Server metrics
- Buttons to activate, deactivate, and restart the servers
- Plot list indicator lights
- Plot metrics
- Buttons to add, edit, and delete growth requirements for plots
- Harvest countdown <br><br>
# HOW IT WORKS:
When the UI is rendered by the backend, JavaScript immediately does 4 things: it loads the current date and time; it loads the growth requirements (if any exists in the database) of plot 0; it "activates" all the plots that have growth requirements stored in the database (it turns their indicator lights green); it asks the backend for plot 0's sensor data, and after receiving them, it puts them into their respective variables in the metrics list. 

JavaScript will re-calculate the current date & time, and the harvest countdown for the currently selected plot, every second. 

Every three seconds, JavaScript will ask the backend for the currently selected plot's sensor data and it will again place the values in their respective variables on the metrics list. 

The values for the sensor data are randomly generated in the backend using a class called "PlotSensorDataReceiver". Each plot will have its own instance of this class. These instances are created before the UI is first rendered (inside the index route). The number of instances that are created are determined by the number of growth requirements in the database (each requirement is mapped to a plot). When an instance is created, it is set to "listen" for new sensor data. Behind the scenes, all this does is it creates a new thread in Python that contains a loop which continuously generates random sensor data for the instance – this is supposed to simulate the master computer receiving sensor data from the server nodes. Whenever JavaScript asks the backend for the currently selected plot's sensor data, what it really means is that the plot's sensor data receiver instance returns a dictionary containing the randomly generated values at that given moment. 

Growth requirements are added to the database by using the add button, and they are updated using the edit button. In both cases, the form inputs are passed to the backend using JavaScript (to avoid page reloads). Behind the scenes, the data is validated before being committed to the database – this data is what makes up a growth requirement. To reiterate, the growth requirements in the database determine the number of PlotSensorDataReceiver instances that are created before the UI is first rendered.

As for the server portion of the UI, all it does for now is change the colors of the indicator lights. When a server is activated, the light turns green, and when deactivated the light turns red. When the server is restarted, the light turns red for a moment and switches back to green. Since each server is mapped to a sensor data variable, I was thinking of making a mechanism that ignores the randomly generated value for a given sensor data variable when that variable’s server node is deactivated. And of course when the server is restarted, the value disappears temporarily.
