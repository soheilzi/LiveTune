# LiveTune 🎶
LiveTune is a Python package designed to allow for parameter adjustment while a program is actively running. This allows ML developers and researchers to change certain variables, data, or the hyperparameters such as learning rate and regularizer while their code is executing to make the task of training an ML project easier. This package allows you to tune the parameters while your code is live from outside the program.

# Installation

### Platform Support
| Platform | Support |
|:-----|:--------:|
| MacOS 🍎 | Supported |
| Linux 🐧 | Supported |
| Windows 🪟 | Untested |

### How to Install

To install, open terminal and run the following PyPi command:
```bash
pip install -i https://test.pypi.org/simple/ LiveTune==0.0.3
```
If PyPi is not installed, please [follow these instructions.](https://packaging.python.org/en/latest/tutorials/installing-packages/)

# Features
There are two primary features available in LiveTune. Live Variables and Live Triggers. Both of which are identified using the **tag system**.

Every live variable and live trigger must specify a value and a string: the tag associated with it. The tag is how LiveTune can identify which variable a developer is attempting to change.

When an instance of a program using LiveTune is started, LiveTune will report the instance's port number associated with the program in the terminal.

| Feature |  Type  | Function | Usage
|:-----|:--------:|:--------:|:--------:|
| Live Variable   | int, char, string, float, boolean | A variale that can be modified at runtime. | Adjust hyper parameters, data sets, parameters, user information, etc.
| Live Trigger   |  boolean | A boolean that is always false. When triggered, stays true for one call. | Trigger a function, loop, or stop code remotely.


# How to Use
Implementing LiveTune in your codebase could not be easier.

First install the package via the following command:

```bash
pip install -i https://test.pypi.org/simple/ LiveTune==0.0.3
```

## Setting up Live Variables 
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

**Note:** If a variable is created *based* off of a Live Variable, it will not adjust if the Live Variable is updated. For example, if the variable ranking2 = ranking + 5, updating the value of ranking will *not* update the value of ranking2.

## Setting up Live Triggers
A live trigger is a boolean that will always return *False* when called. If a developer "triggers" it, the boolean will return *True* the next time it is called. 

First, import liveVar from LiveTune:
```python
from LiveTune import liveTrigger
```

To create a Live Trigger, create a new variable in the liveTrigger class.

```python
myTrigger = liveTrigger('TAG')
```

Example usage:
```python
stopLoop = liveTrigger('stop')
```

## Updating a LiveTune Variable
The unique advantage of using LiveTune for variables is the ability to adjust the variables in the middle of the program with ease.

When you start your program, LiveTune will assign your instance to a port on the machine. This port is where tags are temporarily associated with ports on the client.
```bash
Port number for liveVar dictionary: 63573
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
We're still testing, so please fill out the following feedback form if you find any bugs or have feature requests: [MISSING LINK]

We hope this package will help innovate and streamline your ML trainings! If you find this useful in other cases, please let us know as well.

✋

|

|

🎤 (mic drop)
