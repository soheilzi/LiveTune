from LiveTune.initVar import initVar
import time

# Define two variables
var1 = initVar(0, 12345)
var2 = initVar(5, 12346)
var3 = initVar(5, 12347)

# Sleep for 5 seconds to observe the update behavior
time.sleep(5)

# Access and print the values of the variables
while True:
    print("var1 value:", var1['value'])
    print("var2 value:", var2['value'])
    print("var3 value:", var3['value'])
    time.sleep(1)