# Langton's Ant

<p align="center">
    <img alt="Made with Python" src="https://img.shields.io/badge/Made%20with-Python-3776ab?style=for-the-badge&logo=python">
    <a href="./LICENSE">
        <img alt="License file" src="https://img.shields.io/github/license/Pagliacii/langton-ant?style=for-the-badge">
    </a>
</p>

See [Langton's Ant](https://en.wikipedia.org/wiki/Langton%27s_ant) on wikipedia for more details.

## Usage

```shell
$ git clone https://github.com/Pagliacii/langton-ant
$ cd langton-ant
# Usage: langton.py [rules_file | ./rules/origin.json] [fps | 2]
$ python langton.py
```

## Rules Template

```python
{
    "default": "white",      # Default color, uses to generate the empty plane
    "white": {
        "symbol": "\u2b1b",  # A symbol to represent this cell
        "turn": "right",     # Turn left or right
        "flip": "black"      # Flips to this new color
    },
    "black": {
        "symbol": "\u2b1c",
        "turn": "left",
        "flip": "white"
    }
}
```

## Screencast

![screencast](assets/langton-ant.gif)

## Highway Pattern

![highway](assets/highway.png)
