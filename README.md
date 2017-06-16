# Granblue Autopilot
Granblue Autopilot is an open-source grinding/farming bot for Granblue Fantasy licensed under the [MIT License](LICENSE).

# Table of Contents
* [Disclaimer](#disclaimer)
* [Introduction](#introduction)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Building](#building)
  * [Starting the servers](#starting-the-servers)
  * [Using the extension](#using-the-extension)
* [Configuration](#configuration)
  * [Command server](#command-server)
  * [Control server](#control-server)
* [Scenarios](#scenarios)
  * [Writing a scenario](#writing-a-scenario)
  * [Using the scenario](#using-the-scenario)
  * [Actions](#actions)
* [License](#license)

## Disclaimer
This is just a fun project that I did while playing the game. Use it at your own risk.

The bot ***may be*** detectable since it involves an extension to run on your Google Chrome browser instead of using less detectable but more CPU heavy solution such as image processing with OpenCV. However, the extension itself does virtually nothing other than responding to queries from the **command server** and partially controls the page so it is less likely to trigger the anti-cheat.

As according to the [MIT License](LICENSE), this software is provided **"AS IS"** and comes without any warranty. I'm ***not*** responsible for any kind of damage or losses caused by the usage of this software.

All the servers run on your local machine and the ports are not exposed to public; it only listens to your local machine.

## Introduction
This is a complete rewrite of [the previous bot](https://github.com/Frizz925/gbf-raid-bot) that heavily relies on OpenCV library and also a working application that is derived from the incomplete [Mary Bot](https://github.com/Frizz925/mary-bot).

It lets you to grind in the game with preset scenarios written using JavaScript. The example scenario can be found [here](server/scenarios/pina_hazard.js) which is used to automatically farm the Extreme and Nightmare stages in [Cinderella Fantasy: Piña Hazard](https://gbf.wiki/Cinderella_Fantasy:_Pi%C3%B1a_Hazard) event. 

## Getting Started
The bot consists of 3 separate applications:
* **Chrome Extension** (*extension*) - Partially controls the page and respond all queries from the command server.
* **Command Server** (*server*) - Low-latency server using Node.js and Socket.IO where most of the application logic runs. Also queries the extension and make calls to the control server when needed.
* **Control Server** (*controller*) - Python Flask server which controls the mouse and keyboard inputs.

The **control server** is tightly coupled with your operating system. Currently it only works on Windows NT using [pywin32](https://sourceforge.net/projects/pywin32/).

### Prerequisites
* [Node.js 6.0+](https://nodejs.org/)
* [Python 3.5](https://www.python.org/)

### Building
```sh
# Install Node.js depedencies using npm
npm install

# Install Python dependencies using pip
pip install -r requirements.txt

# Build the server and extension
npm run build
```

### Starting the servers
```sh
# Start the servers
npm start
```

### Using the extension
* Open your [Google Chrome's Extensions](chrome://extensions) page.
* Check the **Developer mode** checkbox on the top right of the page.
* Click the **Load unpacked extension...** button and browse to the `extension` folder in the project directory.
* Open [Granblue Fantasy](http://game.granbluefantasy.jp/) in your browser.
* Click the bot icon and press the **Start** button inside the popup to start the bot.

## Configuration
The configurations are stored inside the `config.ini` file of each application.

### Command server
| Options       | Default | Description |
|---------------|---------|-------------|
| listener_port | 49544   | The port of the command server. |
| controller_port | 49545 | The port of the control server. |
| action_timeout_in_ms | 60000 | Maximum amount of time in milliseconds before an action (eg. clicks) timed out and generates an error. |
| scenario | pina_hazard | The name of the scenario that the bot will use. |

### Control server
| Options       | Default | Description |
|---------------|---------|-------------|
| listener_port | 49544   | The port of the control server. |
| window_title  | Granblue Fantasy - Google Chrome | The title of the browser window to lookup. |
| input_tween | easeInOutCubic | Tween function to move the cursor used by [PyAutoGUI](https://github.com/asweigart/pyautogui). List of tween functions is listed [here](https://github.com/asweigart/pyautogui/blob/master/pyautogui/tweens.py). |

## Scenarios
The bot uses scenario to determine what action it should take based on the logic and state of the game. The scenario itself is written in JavaScript and stored in the `server/scenarios` directory. Example of a scenario can be found [here](server/scenarios/pina_hazard.js).

### Writing a scenario
All scenarios must be stored inside the `server/scenarios` directory. The scenario will be treated as a module by the **control server** using `require()`. The scenario itself must exports an array of actions.

Here are some ways to write the action inside a scenario:
```js
// The simplest way to write the action is by using string
String action_name

// More general way to write the action is by using array
// This is for single argument
[String action_name, String|Number arg] 

// This is for multiple arguments
[String action_name, Array<String|Number> array_of_args]

// The most advanced use is to call the action and use a function to determine what next action should be taken
[
    String action_name, 
    Array<String|Number> array_of_args, 
    Function success_callback(next, actions, result),
    Function error_callback(next, actions, error)
]
```

Consider the following scenario inside a battle:
```
1. From 3rd character, use the 4th skill
2. From 1st character (MC), use the 2nd skill
3. Use any available summon
4. Turn on the Charge Attack
5. Attack
```

The scenario above can be written as the following:

```js
module.exports = [
    ["battle.skill", "3-4"],
    ["battle.skill", [1, 2]],
    "battle.summon",
    ["battle.ca", true],
    "battle.attack"
];
```

Some actions' arguments can be written in different ways such as for `battle.skill`. Notice how the the arguments for the `battle.skill` can be written either as a single string or an array of numbers.

### Using the scenario
The filename of the scenario is used to identify the scenario that the bot will use. For example, to load the scenario saved as `server/scenarios/pina_hazard.js`, you should have the following options inside of the **command server** config file:
```ini
[server]
# ...
scenario = pina_hazard
# ...
```
Notice that the value of the option as `pina_hazard` does not include the extension (`.js`) and the directory path (`server/scenarios`).

### Actions
The bot currently has limited number of actions (it mostly revolves around mouse clicks). The actions assume that the **Viramate** extension is installed with quick skill buttons and auto-skip/next enabled.

*This section is incomplete*

## License
This software is licensed under the [MIT License](LICENSE)
