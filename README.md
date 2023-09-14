# LiveTune: Dynamic Parameter Tuning 🎶

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
pip install -i https://test.pypi.org/simple/ LiveTune==0.0.4
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

**Note:** Derived variables from a Live Variable won't auto-update. For instance, if ranking2 = ranking + 5, modifying ranking won't affect ranking2.

## Setting up Live Triggers
A live trigger is a boolean that will always return *False* when called. If a developer "triggers" it, the boolean will return *True* the next time it is called. 

First, import liveVar from LiveTune:
```python
from LiveTune import liveTrigger
myTrigger = liveTrigger('TAG')
```

Example usage:
```python
stopLoop = liveTrigger('stop')
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


__NOTE TO SOHEIL: WE NEED TO TEST THIS:__

LiveTune can also be used in your Python programs. You can import the tune tool by using:
```bash 
from LiveTune import tools as lt
```
You can now use *lt.tune* within your program. This can include a separately ran program that is started after the original program.

## Unit Tests

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


## Thank you for using LiveTune!
We're still early in testing, so please [fill out the feedback form if you find any bugs or have feature requests.](https://docs.google.com/forms/d/e/1FAIpQLSfHbM8Jy8w8EDZu_mEV0pH2qtqn3jplsB45KlmVsj6LORrBQQ/viewform?usp=sf_link)

Thank you for using LiveTune! If it's been beneficial to your work, please consider citing our package in your publications. Your support helps us continue our efforts and assists others in discovering LiveTune. We appreciate your acknowledgment.
