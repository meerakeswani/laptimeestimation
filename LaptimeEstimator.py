import pandas as pd
import numpy as np
import requests
import csv
from datetime import datetime

SOLAR_RAY_EFFICIENCY_PERCENTAGE = 0.254
ARRAY_SIZE = 3.98
LAP_LENGTH = 3.15 #arbitrary value
BATTERKWH = 4.68

#INITIALIZE ARRAYS
solarPowerArray = []
energyInArray = []
targetSpeedArray = []
lapTimeArray = []
energyOutArray = []
powerEstimatedArray = []
SOCEstimatedArray = []
lowerBoundSpeedArray = []
upperBoundSpeedArray = []


# Read the CSV file
df = pd.read_csv('/Users/meerakeswani/Downloads/calsoltest.csv')
dfGHI = pd.read_csv('/Users/meerakeswani/Downloads/calsoltest.csv')

# Output the DataFrame

#GHI_Array = df['GHI']
#GHI_Array = GHI_Array[~np.isnan(GHI_Array)]
api_key = "j_sPiCuWG1VYY_MknTU5hA8aHryohaQk"
latitude = 37.871523  # Replace with your location's latitude
longitude = -122.273042  # Replace with your location's longitude

url = f'https://api.solcast.com.au/world_radiation/estimated_actuals?latitude={latitude}&longitude={longitude}&format=json&api_key={api_key}'

response = requests.get(url)


if response.status_code == 200:
    try:
        data = response.json()
        ghi_data =[entry['ghi'] for entry in data['estimated_actuals']]
        time_data = [entry['period_end'] for entry in data['estimated_actuals']]
        print("Data retrieved successfully:", ghi_data)
    except requests.JSONDecodeError:
        print("Error: Response is not in JSON format.")
else:
    print("Error fetching data:", response.status_code, response.text)



dfGHI = pd.DataFrame()

# Add the new data as a column
dfGHI['Time'] = time_data
dfGHI['GHI_new'] = ghi_data  # Ensure ghi_data has the same length as the existing DataFrame


# Save the updated DataFrame back to the CSV file
dfGHI.to_csv('/Users/meerakeswani/Downloads/calsoltestGHI.csv', index=False)




for ghi_val in ghi_data:
    solarPowerArray.append(ghi_val*SOLAR_RAY_EFFICIENCY_PERCENTAGE*ARRAY_SIZE)



for solarPowerVal in solarPowerArray:
    energyInArray.append(solarPowerVal/2)

user_input = int(input("Please enter a speed value (an integer in mph): "))
speedArray = df['Speed']


targetSpeedArray.append(user_input)

#speedArray = speedArray[~np.isnan(speedArray)]





#targetSpeedArray = df['Target Speed']


for targetSpeed in targetSpeedArray:
    lowerBoundSpeed = 0
    diff = 1000
    for speed in speedArray:
        if (abs(targetSpeed-speed) < diff):
            lowerBoundSpeed = speed
            diff = abs(targetSpeed-speed)
    lowerBoundSpeedArray.append(lowerBoundSpeed)


for speed in lowerBoundSpeedArray:
    upperBoundSpeedArray.append(speed + 2.5)
        
zephyrPowerArray = df['Zephyr Power']
zephyrPowerArray = zephyrPowerArray[~np.isnan(zephyrPowerArray)]
excaliburScalingArray = df['Excalibur Scaling']
excaliburScalingArray = excaliburScalingArray[~np.isnan(excaliburScalingArray)]

excaliburPowerArray = []
for i in range(len(zephyrPowerArray)):
    excaliburPowerArray.append(excaliburScalingArray[i] * zephyrPowerArray[i])



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

for speed in speedArray:
    lapTimeArray.append(LAP_LENGTH/(speed/60))

for power in powerEstimatedArray:
    for energyIn in energyInArray:
        energyOutArray.append(power/2 - energyIn)


## CHECK FOR FIRST VALUE
prevSOC = 70 #Change later
for energyOut in energyOutArray:
    currentSOC = prevSOC - (energyOut / BATTERKWH * 1000)
    SOCEstimatedArray.append(currentSOC)
    prevSOC = currentSOC

#calculation for whole day
energyInTotal = 0
for i in range(0,16):
    energyInTotal += energyOutArray[i]
    
energyOutTotal = 0
for i in range(0,16):
    energyOutTotal += energyOutArray[i]


print( "target lower bound speed: ", lowerBoundSpeedArray[0], " mph")
print( "target upper bound speed: ", upperBoundSpeedArray[0], " mph")
print("power estimated: ", powerEstimatedArray[0], " W")
print("energy in for whole day: ", energyInTotal)
print("energy out for whole day: ", energyOutTotal)


