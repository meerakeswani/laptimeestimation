import pandas as pd

SOLAR_RAY_EFFICIENCY_PERCENTAGE = 0.254 
ARRAY_SIZE = 3.98
LAP_LENGTH = 3.15 #arbitrary value
BATTERKWH = 4.68


# Read the CSV file
df = pd.read_csv('/Users/meerakeswani/Downloads/FSGP\ 2024\ Spreadsheeting\ -\ Scrutineering\ Affected\ Data.csv')

# Output the DataFrame

GHIArray = df['GHI'] 

solarPowerArray = [] 

for ghi_val in GHI_Array: 
    solarPowerArray.append(ghi_val*SOLAR_RAY_EFFICIENCY_PERCENTAGE*ARRAY_SIZE)


energyInArray = [] 

for solarPowerVal in solarPowerArray: 
    energyInArray.append(solarPowerVal/2) 

speedArray = df['Speed']
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
targetSpeedArray = df['Target Speed'] 
for targetSpeed in targetSpeedArray: 
    lowerBoundSpeed = 0
    diff = 1000 
    for speed in speedArray: 
        if (abs(targetSpeed-lowerBoundSpeed) < diff): 
            lowerBoundSpeed = targetSpeed 
            diff = abs(targetSpeed-lowerBoundSpeed) 
    lowerBoundSpeedArray.append(lowerBoundSpeed) 

upperBoundSpeedArray = [] 
for speed in lowerBoundSpeedArray: 
    upperBoundSpeedArray.append(speed + 2.5) 
        
zephyrPowerArray = df['Zephyr Power'] 
excaliburScalingArray = df['Excalibur Scaling'] 

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
    powerEstimatedArray.append( (closestUpperBoundPowerArray[i] - closestLowerBoundPowerArray[i]) * (targetSpeedArray[i] - lowerBoundSpeedArray[i])/(upperBoundSpeedArray[i] - lowerBoundSpeedArray[i]) + closestLowerBoundPowerArray[i]



