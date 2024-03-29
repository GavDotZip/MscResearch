import traci
import numpy as np
import pandas as pd
import time

# Command to start SUMO simulation:
# sumo-gui to open gui.
sumo_cmd = ["sumo", "-c", "C:/Users/gavin/PycharmProjects/applyingRLtoUTM/sumoDocs/singleIntersection.sumocfg"]
traci.start(sumo_cmd)

# Initialize lists for storing simulation data
BigData = []
vehicleData = []


# Function to flatten list into 2D readable data
def flatList(_2d_list):
    """
    Flatten a 2D list into a 1D list.
    """
    flattenedList = []
    for element in _2d_list:
        if type(element) is list:
            for item in element:
                flattenedList.append(item)
        else:
            flattenedList.append(element)
    return flattenedList


# Extract and process simulation data
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    vehicles = traci.vehicle.getIDList()
    speeds = [traci.vehicle.getSpeed(vehicle) for vehicle in vehicles]
    emissions = [traci.vehicle.getCOEmission(vehicle) for vehicle in vehicles]
    fuel = [traci.vehicle.getFuelConsumption(vehicle) for vehicle in vehicles]
    noise = [traci.vehicle.getNoiseEmission(vehicle) for vehicle in vehicles]
    wait = [traci.vehicle.getWaitingTime(vehicle) for vehicle in vehicles]
    for i in range(0, len(vehicles)):
        step = traci.simulation.getTime()
        system_total_waiting_time = sum(wait)
        system_total_emissions = sum(emissions)
        system_total_fuel_consumption = sum(fuel)
        system_total_noise_caused = sum(noise)
        system_total_petrol_cost = sum(fuel) * 162.9 / 100
        system_total_diesel_cost = sum(fuel) * 151.8 / 100
        system_mean_waiting_time = 0.0 if len(vehicles) == 0 else np.mean(wait)
        system_mean_speed = 0.0 if len(vehicles) == 0 else np.mean(speeds)

        # Add data variables to a list and pack into flat list
        vehicleList = [step, system_total_waiting_time, system_total_emissions, system_total_fuel_consumption,
                       system_total_petrol_cost, system_total_diesel_cost, system_total_noise_caused,
                       system_mean_waiting_time, system_mean_speed]

    packBigDataLine = flatList([vehicleList])
    BigData.append(packBigDataLine)

# Close the simulation
traci.close()

# Set column names for Excel file
columnnames = ["step", "system_total_waiting_time", "system_total_emissions",
               "system_total_fuel_consumption", "system_total_petrol_cost", "system_total_diesel_cost",
               "system_total_noise_caused", "system_mean_waiting_time", "system_mean_speed"]

# Convert data to DataFrame and save to Excel
dataset = pd.DataFrame(BigData, index=None, columns=columnnames)
dataset.to_excel("dqnresults/PhaseOneTraditionalFixedStats.xlsx", index=False) # Change based on algorithm used (if any)
time.sleep(5)
