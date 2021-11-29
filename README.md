![Firelight](doc/firelight-dark.png#gh-dark-mode-only)
![Firelight](doc/firelight-light.png#gh-light-mode-only)


## About Firelight
[Firelight](https://github.com/roshie548/firelight) is an open source bias lighting program which syncs up colored lights to the contents of your screen or TV, providing an immersive experience.

![Demo Firelight](doc/firelight-demo.gif)

## Installation
To install:
```
pip install firelight-lighting
```

To install directly from Github:
```
git clone https://github.com/roshie548/firelight.git
cd firelight
pip install .
```

## Usage
Currently, Firelight only supports LIFX lights. To start the application, simply run:
```
firelight lifx
```
Firelight will automatically discover the lights connected to your WiFi network and will start syncing their colors to your screen. Please make sure that the lights are on to see the effect. You can exit the application at any time by pressing `Ctrl + C`.

## Asking for help or requesting features
If you need some help or would like more features added, please open an issue.
