# Track Switching Game v0.1
You are in control of the train tracks of a train station and must quickly route incoming trains to their desired platforms!

![Screenshot of Freiburg level](https://github.com/theMashUp/track-switching-game/assets/screenshot.png?raw=true "Screenshot of Freiburg level")

## Getting started
To play the game, first clone this repository.
Then, install the pygame library.
Finally, run main.py:
```Python
python main.py -l levels/freiburg.json
```

## Features
- The game is composed of tracks, some of which you can switch by clicking on them. Switching is only possible when no train is currently on the tile.
- Portals: tracks with a blue background and a letter. Trains can enter or leave the playing field from portals.
- Platforms: tracks with a green background and a number. Incoming trains want to stop at a platform before leaving again.
- Scoring: When the train has left the playing field, +1 point for a correct platform, +1 point for a correct exit portal.
- Speed increase: After certain scores, the speed of the game increases.
- Game over: no game over currently.

## Configuration
### Level
*-l, --level*

Path to level .json file.

### Debug
*-d, --debug*

Activate debug mode, which displays more information in the console.

## Contributing
As this is a personal project, I will not be entertaining external contributions to features of the game. However, please feel free to suggest new features or report bugs.
### Creating a new level
Although it is very limited at the moment, custom levels can be created. Please note that you might that the game is not robust for funky levels.
Simply copy the freiburg.json file in the levels folder, and let your imagination flow! Here are some guidelines:
- Track tiles are defined as an matrix of strings. An empty string represents an empty tile. To add rails, add a two-letter combination of m (middle), u (up), and d (down). "dm" means a track starting at the bottom left corner, and ending in the middle.
- To make a switching track, add another two-letter string to the tile, separated by a plus. For example, the "mm+md" string would lead to a tile that starts left in the middle (m), then splits in the middle to go straight (m) or down (d).
- To identify a track as a portal, add a "+A" to the string, where "A" is the portal designator. Portals should be all the way right or left, and only one portal per designation.
- To identify a track as a platform, add a "+1" to the string, where "1" is the platform designator. Platforms should be three tiles long, and adjacent.
- The game is not bright enough to know which portal(s) can lead to which platforms, this must be specified in the level file under the variable "platform_portals_connections".

## Licensing
Copyright (c) 2022 Jonathan Larochelle