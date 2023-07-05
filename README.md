# LiveTune
Python package for ML developers and researchers to change certain variables while their code is executing to make the task of training a ML project easier. This package will allow you to tune some parameters while your code is live from outside of the program

# Usage
The target.py script provided contains examples of setting variables up to be able to be tuned during the training. Upon starting the script, the program will loop through printing and incrementing the numbers to simulate the process of training an ML project.

To update the variables, set the variables to be changed and the new replacement variables in update.py and run update.py while the program is running. The variables will change accordingly.