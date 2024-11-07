import pandas as pd
import numpy as np 
import requests
import csv

SOLAR_RAY_EFFICIENCY_PERCENTAGE = 0.254 
ARRAY_SIZE = 3.98
LAP_LENGTH = 3.15 #arbitrary value
BATTERKWH = 4.68


# Read the CSV file
df = pd.read_csv('./Downloads/calsoltest.csv')

# Output the DataFrame

#GHI_Array = df['GHI'] 
#GHI_Array = GHI_Array[~np.isnan(GHI_Array)]

api_url = "https://api.solcast.com.au/world_pv_power/estimated_actuals?latitude=37.871523&longitude=-122.273042&capacity=5&tilt=33&azimuth=180&hours=168"
api_key = "hL4glLjAEaCIASrHqN7eIIk5UwiMmg9q"

if response.status_code == 200:
    data = response.json() 

ghi_values = [entry.get("ghi") for entry in data.get("forecasts", [])]

    # Write GHI values to a CSV file with a single column
    with open("ghi_values.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["GHI"])  # Write header

        for ghi in ghi_values:
            writer.writerow([ghi])  # Write each GHI value as a single-row entry

solarPowerArray = [] 

for ghi_val in GHI_Array: 
    solarPowerArray.append(ghi_val*SOLAR_RAY_EFFICIENCY_PERCENTAGE*ARRAY_SIZE)


energyInArray = [] 

for solarPowerVal in solarPowerArray: 
    energyInArray.append(solarPowerVal/2) 

user_input = int(input("Please enter a speed value (an integer in mph): "))
speedArray = df['Speed']

targetSpeedArray = []
targetSpeedArray.append(user_input)

#speedArray = speedArray[~np.isnan(speedArray)]

lapTimeArray = []
for speed in speedArray: 
    lapTimeArray.append(LAP_LENGTH/(speed/60)) 

energyOutArray = []
powerEstimatedArray = []
for power in powerEstimatedArray: 
    for energyIn in energyInArray:
        energyOutArray.append(powerEstimatedArray/2 - energyIn) 

SOCEstimatedArray = []
## CHECK FOR FIRST VALUE 
for energyOut in energyOutArray:
    currentSOC = prevSOC - (energyOut / BATTERKWH * 1000)
    SOCEstimatedArray.append(currentSOC)
    prevSOC = currentSOC

lowerBoundSpeedArray = [] 
#targetSpeedArray = df['Target Speed']


for targetSpeed in targetSpeedArray:
    lowerBoundSpeed = 0
    diff = 1000 
    for speed in speedArray:
        if (abs(targetSpeed-speed) < diff):
            lowerBoundSpeed = speed
            diff = abs(targetSpeed-speed)
    lowerBoundSpeedArray.append(lowerBoundSpeed) 

upperBoundSpeedArray = [] 
for speed in lowerBoundSpeedArray: 
    upperBoundSpeedArray.append(speed + 2.5) 
        
zephyrPowerArray = df['Zephyr Power'] 
zephyrPowerArray = zephyrPowerArray[~np.isnan(zephyrPowerArray)]
excaliburScalingArray = df['Excalibur Scaling'] 
excaliburScalingArray = excaliburScalingArray[~np.isnan(excaliburScalingArray)]

excaliburPowerArray = [] 
for i in range(len(zephyrPowerArray)): 
    excaliburPowerArray.append(excaliburScalingArray[i] * zephyrPowerArray[i]) 


powerEstimatedArray = [] 

closestUpperBoundPowerArray = [] 

for i in range(len(upperBoundSpeedArray)): 
    speedIndex = 0 
    diff = 1000 
    for j in range(len(speedArray)): 
        if ( (abs(upperBoundSpeedArray[i]-speedArray[j])) < diff ): 
            diff = abs(upperBoundSpeedArray[i]-speedArray[j]) 
            speedIndex = j 

    closestUpperBoundPowerArray.append(excaliburPowerArray[speedIndex]) 


closestLowerBoundPowerArray = [] 

for i in range(len(lowerBoundSpeedArray)): 
    speedIndex = 0 
    diff = 1000 
    for j in range(len(speedArray)): 
        if ( (abs(lowerBoundSpeedArray[i]-speedArray[j])) < diff ): 
            diff = abs(lowerBoundSpeedArray[i]-speedArray[j]) 
            speedIndex = j 

    closestLowerBoundPowerArray.append(excaliburPowerArray[speedIndex]) 
    
    
for i in range(len(closestUpperBoundPowerArray)): 
    powerEstimatedArray.append( (closestUpperBoundPowerArray[i] - closestLowerBoundPowerArray[i]) * (targetSpeedArray[i] - lowerBoundSpeedArray[i])/(upperBoundSpeedArray[i] - lowerBoundSpeedArray[i]) + closestLowerBoundPowerArray[i])



print( "target lower bound speed: ", lowerBoundSpeedArray[0], " mph")
print( "target upper bound speed: ", upperBoundSpeedArray[0], " mph")
print("power estimated: ", powerEstimatedArray[0], " W")

