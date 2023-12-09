![LiveTune(Github)](https://github.com/soheilzi/LiveTune/assets/33820269/ffad7937-4bf7-4b1f-aa7f-2921c4007abf)
## Dynamic Parameter Tuning 🎶

LiveTune is a cutting-edge Python package that empowers Machine Learning developers and researchers to adjust parameters in real-time while their program is running. Seamlessly modify variables, data, or hyperparameters, such as learning rate and regularizer, without interrupting your code execution. Experience the freedom to fine-tune your ML projects on-the-fly.

## Installation

### Platform Compatibility

| Platform | Status |
|:--------|:------:|
| MacOS 🍎 | Supported |
| Linux 🐧 | Supported |
| Windows 🪟 | Not Yet Tested |

### Installation Guide

1. Ensure you have PyPi installed. If not, [follow these instructions](https://packaging.python.org/en/latest/tutorials/installing-packages/).
2. Execute the following command in your terminal:
```bash
pip install LiveTune
```

## Key Features

LiveTune offers two primary features: **Live Variables** and **Live Triggers**. Both are managed using our intuitive **tag system**.

Upon starting a program that integrates LiveTune, the terminal will display the port number associated with that program instance.

| Feature | Data Types | Description | Use Cases |
|:-------|:----------:|:-----------:|:---------:|
| Live Variable | int, char, string, float, boolean | Modifiable variables during runtime. | Hyperparameters, datasets, user info adjustments, etc. |
| Live Trigger | boolean | A boolean that, when triggered, returns true for a single call. | Remotely initiate functions, loops, or halt code. |


## Integration Guide

### Setting up Live Variables 
A live variable is an integer, char, string, float, or boolean that is able to be changed in the middle of the program by using a command in the terminal or in a different program.

First, import liveVar from LiveTune:
```python
from LiveTune import liveVar
```

To create a Live Variable, create a new variable in the liveVar class.

```python
myVariable = liveVar(INITIAL_VALUE, 'TAG')
```

Example usage:
```python
ranking = liveVar(100, 'ranking')
```

Live Variables can be used just like normal variables of its type, so feel free to call the variable as needed. 

To avoid resource loss or unnecessary recompiling, liveVar includes a **'changed' method** that returns True or False if the Live Variable has been changed since the last time 'changed' was called in a running instance. 

Example usage:
```python
if myVariable.changed():
    print("This variable has changed!")
```


**Note:** Derived variables from a Live Variable won't auto-update. For instance, if ranking2 = ranking + 5, modifying ranking won't affect ranking2.

## Setting up Live Triggers
A live trigger is a boolean that will always return *False* when called. If a developer "triggers" it, the boolean will return *True* the next time it is called. It can be used to trigger functions, and subroutines. 

First, import liveVar from LiveTune:
```python
from LiveTune import liveTrigger
myTrigger = liveTrigger('TAG')
```

Example usage:
```python
stopLoop = liveTrigger('stop')
while(not stopLoop()):
    pass
```

```python
save = liveTrigger('save')

while training:
    if save():
        save_subroutine()
...
```

## Updating a LiveTune Variable

Upon program initiation, LiveTune assigns a port to your instance. This port links tags to client ports temporarily.
```bash
[LiveTune] Port number for the LiveTune dictionary: 61629
```

To update a variable, use the **tune** command in the terminal or in an external program.


The tune command has a few settings to ensure the correct variable is changed properly.
| Setting | Description | Required | Example
|:-----|:--------:|:--------:|:--------:|
| --port / -p | The port number given by LiveTune above, separate per instance. | Always | --port 63573
| --tag / -t | The developer-set tag string for the variable. Used to identify the variable. | Always | --tag ranking
| --value / -v | The new value for the variable-must match the type of the original (e.g. must be an int if originally an int) | Live Variables only | --value 200
| --trigger / -tr |  LiveTriggers will not "trigger" if this setting isn't included. | Live Triggers only | --trigger

Example terminal usage:
```bash 
tune --value 10 -t myVariable -p 13451
```

```bash 
tune --tag myTrigger --port 13451 -tr
```

You can also update livetune variables using their update method.
example:
```python
myVariable.update(new_value)
```


## Contributing to LiveTune
Those interested in adding features to the package may submit a pull request. Please keep individual improvements to their own pull requests.
Please maintain consistent code format when contributing to ensure the package remains easily understandable for future contributors.

1. Fork the project
2. Create your feature branch `git checkout -b my-new-change`
3. Commit your changes `git commit -am 'Added new feature'`
4. Push to the branch `git push origin my-new-change`
5. Run the Unit Tests specified in the section below
6. Submit a pull request

All contributors should run the Unit Tests below to test their changes.


### Unit Tests

This repository contains a **tests.py** file in the tests folder. Clone this repo by using:
```bash
git clone https://github.com/soheilzi/LiveTune.git
```

Navigate to the LiveTune repository.
```bash
cd LiveTune
```

Ensure Python3 is installed on your computer and run the tests:
```bash
python3 LiveTune/tests/tests.py
```

If all tests pass, LiveTune is working correctly. If contributing, please run all tests before submitting a pull request.

## Authors

- Soheil Zibakhsh Shabgahi - [szibakhshshabgahi@ucsd.edu](mailto:szibakhshshabgahi@ucsd.edu)
- Aiden Tabrizi - [atabrizi@ucsd.edu](mailto:atabrizi@ucsd.edu)

### Contact
If you are interested in using the code for commercial use, please contact [innovation@ucsd.edu](mailto:innovation@ucsd.edu)

## Thank you for using LiveTune!
We're still early in testing, so please [fill out the feedback form if you find any bugs or have feature requests.](https://docs.google.com/forms/d/e/1FAIpQLSfHbM8Jy8w8EDZu_mEV0pH2qtqn3jplsB45KlmVsj6LORrBQQ/viewform?usp=sf_link)

Thank you for using LiveTune! If it's been beneficial to your work, please consider citing our paper in your publications. 
```@article{shabgahi2023livetune,
  title={LiveTune: Dynamic Parameter Tuning for Training Deep Neural Networks},
  author={Shabgahi, Soheil Zibakhsh and Sheybani, Nojan and Tabrizi, Aiden and Koushanfar, Farinaz},
  journal={arXiv preprint arXiv:2311.17279},
  year={2023}
}
```
Your support helps us continue our efforts and assists others in discovering LiveTune. We appreciate your acknowledgment.
