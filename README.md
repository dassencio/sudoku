[![Build Status](https://travis-ci.org/dassencio/sudoku.svg?branch=master)](https://travis-ci.org/dassencio/sudoku/)


Description
===========

A Sudoku puzzle solver (written in Python 3) which models and solves the puzzle
as an Integer Linear Programming (ILP) problem.


License
=======

All code from this project is licensed under the GPLv3. See the `LICENSE` file
for more.


Required Libraries
==================

This project needs the [PuLP](https://pypi.python.org/pypi/PuLP) module to work.
On Ubuntu/Debian, you can install this module by running the following command
on a terminal:

	sudo apt-get install python3-pulp


Instructions
============

This projects illustrates how a Sudoku puzzle can be formulated as an Integer
Linear Programming problem. It contains two main files:

- `sudoku.py`: a self-contained module with all the functionality needed to
   define and solve a puzzle
-  `sudoku-solver`: an executable script which exemplifies how `sudoku.py` can
   be used to solve a puzzle.

By default, `sudoku-solver` takes its input from `stdin` and outputs the solved
puzzle on `stdout`. To solve a Sudoku puzzle, run `./sudoku-solver` and provide
the following:

- number of rows and columns on each puzzle block in one line (e.g. `2 3`)
- for each puzzle row, a line such as `_ _ _ 4 5 _` specifying the initial
  state of the row; initially unknown values can be represented using any
  non-integer character or string (e.g. `_`, `__`, `?` or `*`)

As an example, the following input specifies a puzzle with 2×3 blocks, i.e.,
each block contains 2 rows and 3 columns, and the puzzle contains 6 rows/columns
in total:

	2 3
	_ _ _ 2 _ _
	_ _ _ 4 5 _
	_ 3 4 _ _ _
	_ _ _ 1 4 _
	_ 6 1 _ _ _
	_ _ 5 _ _ _

The output is the solution to the puzzle:

	5 4 6 2 3 1
	2 1 3 4 5 6
	1 3 4 5 6 2
	6 5 2 1 4 3
	4 6 1 3 2 5
	3 2 5 6 1 4


Running the Validation Tests
============================

This repository comes with tests which can be used to validate the solver. These
tests also illustrate the input format discussed above.

Each test contains an associated input file (e.g. `test05.in`) which defines the
puzzle, and an associated output file (e.g. `test05.out`) which specifies the
expected output contaning the solution to the puzzle. On Linux, you can execute
these tests by entering the `tests` subdirectory and running the following
command:

	./run-tests


Contributors & Contact Information
==================================

Diego Assencio / diego@assencio.com
