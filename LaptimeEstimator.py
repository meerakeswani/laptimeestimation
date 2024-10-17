import pandas as pd

SOLAR_RAY_EFFICIENCY_PERCENTAGE = 0.254 
ARRAY_SIZE = 3.98
LAP_LENGTH = 3.15 #arbitrary value

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


