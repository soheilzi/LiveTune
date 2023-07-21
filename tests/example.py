import LiveTune as lt

# Define two variables
var1 = lt.initVar('var1', 0, 12345)
var2 = lt.initVar('var2', 5, 12346)

# Start the threads for variable updates
var1.start()
var2.start()

# At this point, the threads are running and updating the variables in the background.
# You can now use the variables in your new program as needed, and they will be updated when the update command is ran.
