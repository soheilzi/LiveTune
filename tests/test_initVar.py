from initVar import initVar
import time

# Define two variables
var1 = initVar('var1', 0, 12345)
var2 = initVar('var2', 5, 12346)

var1.start()
var2.start()

# Sleep for 5 seconds to observe the update behavior
time.sleep(5)

# Access and print the values of the variables
print("var1 value:", var1['value'])
print("var2 value:", var2['value'])