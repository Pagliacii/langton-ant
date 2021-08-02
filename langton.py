#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# MIT License
#
# Copyright (c) 2021 Pagliacii
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Author:             Pagliacii
# Last Modified By:   Pagliacii
# Created Date:       2021-08-02 10:51:53
# Last Modified Date: 2021-08-02 23:54:35

import json
import random
import sys
import time

from pathlib import Path
from typing import Tuple


class Simulator:
    """A simulator to simlate the Langton's ant behaviors."""

    def __init__(self, rules, row: int = 16, column: int = 32, fps: int = 24) -> None:
        self._ant_pos: Tuple[int] = (
            random.randint(0, row - 1),
            random.randint(0, column - 1),
        )
        # 0 for N, 1 for W, 2 for S, 3 for E
        self._ant_direction: int = random.randint(0, 4)
        self._row = row
        self._column = column
        self._delta = 10 ** 9 // fps

        # Uses emoji to draw the plane
        self._ant = "\N{Ant}"
        self._rules = rules
        self._default_cell = rules["default"]

        # Prepares the init-plane
        self._plane = self._new_plane()

    def _new_plane(self) -> list[list[int]]:
        """Creates a new empty plane."""
        return [
            [self._default_cell for _ in range(self._column)] for _ in range(self._row)
        ]

    def _move_forward(self) -> None:
        row, column = self._ant_pos
        if self._ant_direction == 0:
            self._ant_pos = (row - 1) % self._row, column
        elif self._ant_direction == 1:
            self._ant_pos = row, (column - 1) % self._column
        elif self._ant_direction == 2:
            self._ant_pos = (row + 1) % self._row, column
        else:
            self._ant_pos = row, (column + 1) % self._column

    def _draw(self) -> None:
        """Draws the current plane."""
        for row in range(self._row):
            for column in range(self._column):
                if (row, column) == self._ant_pos:
                    sys.stdout.write(self._ant)
                else:
                    rule = self._rules[self._plane[row][column]]
                    sys.stdout.write(rule["symbol"])
                sys.stdout.flush()
            sys.stdout.write("\n")
            sys.stdout.flush()

    def _erase(self) -> None:
        """Erases the existed plane"""
        for _ in range(self._row):
            self._erase_one_row()
            # Go to the end of previous row
            sys.stdout.write("\033[A")
            sys.stdout.flush()
        sys.stdout.write("\r")
        sys.stdout.flush()

    def _erase_one_row(self) -> None:
        """Erases one row on the plane"""
        sys.stdout.write("\033[2K")
        sys.stdout.flush()

    def _next_plane(self) -> None:
        """Generates the next plane based on two simple rules."""
        rule = self._rules[self._plane[self._ant_pos[0]][self._ant_pos[1]]]
        self._plane[self._ant_pos[0]][self._ant_pos[1]] = rule["flip"]
        if rule["turn"] == "left":
            self._ant_direction = (self._ant_direction + 1) % 4
        else:
            self._ant_direction = (self._ant_direction - 1) % 4
        # Move forward one unit
        self._move_forward()

    def run(self) -> None:
        """Starts this simulator"""
        tic: int = 0
        while True:
            try:
                toc: int = time.perf_counter_ns()
                if tic == 0:
                    # First time
                    tic = time.perf_counter_ns()
                elif toc - tic < self._delta:
                    # Keeps waiting
                    continue
                self._erase()
                # Draws the current plane.
                self._draw()
                # Generates the next plane.
                self._next_plane()
                # Updates the tic time.
                tic = time.perf_counter_ns()
            except KeyboardInterrupt:
                break


if __name__ == "__main__":
    fps = 2
    if len(sys.argv) < 2:
        rules_file = Path.cwd() / "rules/origin.json"
    elif len(sys.argv) == 2:
        rules_file = Path(sys.argv[-1])
    elif len(sys.argv) == 3:
        rules_file = Path(sys.argv[-2])
        fps = int(sys.argv[-1])
    else:
        sys.stderr.write("\N{Cross Mark} \033[31mToo more arguments.\033[0m\n")
        sys.stderr.flush()
        sys.stdout.write(
            f"Usage: {sys.argv[0]} [rules_file=./rules/origin.json] [fps=2]\n"
        )
        sys.stdout.flush()
        sys.exit(1)

    with rules_file.open("r") as f:
        rules = json.load(f)
    simulator = Simulator(rules, row=22, column=54, fps=fps)
    simulator.run()
