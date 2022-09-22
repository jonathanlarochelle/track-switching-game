# Track Switching Game v0.1
You are in control of the train tracks of a train station and must quickly route incoming trains to their desired platforms!

## Getting started
To play the game, first clone this repository.
Then, install the pygame library.
Finally, run main.py:
```Python
python main.py
```

## Features
- The game is composed of tracks, some of which you can switch by clicking on them. Switching is only possible when no train is currently on the tile.
- Portals: tracks with a blue background and a letter. Trains can enter or leave the playing field from portals.
- Platforms: tracks with a green background and a number. Incoming trains want to stop at a platform before leaving again.
- Scoring: When the train has left the playing field, +1 point for a correct platform, +1 point for a correct exit portal.
- Speed increase: After certain scores, the speed of the game increases.
- Game over: no game over currently.

## Configuration
### Debug
*-d, --debug*

Activate debug mode, which displays more information in the console.

## Contributing
As this is a personal project, I will not be entertaining external contributions to features of the game. However, please feel free to suggest new features or report bugs.

## Licensing
Copyright (c) 2022 Jonathan Larochelle