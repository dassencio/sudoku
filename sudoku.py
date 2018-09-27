#!/usr/bin/env python3

"""A module containing tools for solving Sudoku puzzles."""

import pulp


def var_name(i, j, k):
    """Returns a string in the format x_{i,j,k}."""

    return "x_{%d,%d,%d}" % (i, j, k)


def crange(a, b):
    """Returns a range object for the closed interval [a,b]."""

    return range(a, b + 1)


class Sudoku:

    """
    A Sudoku puzzle solver class.

    The dimensions of a Sudoku puzzle are defined by the size of a puzzle
    block. Each block has m rows and n columns. Since each block has m×n
    cells, the total possible number of values a cell can have is N = m*n,
    and since each row or column of the puzzle must have exactly one
    occurrence of each value in 1:N, both the height and width of the puzzle
    are equal to N. This also implies that the puzzle has n blocks on the
    vertical direction and m blocks on the horizontal direction.

    This solver indexes the puzzle cells with pairs of indices (i,j) which
    are assigned as done for matrix entries, i.e., (i,j) = (1,1) represents
    the top-left corner cell of the puzzle. The index i represents the
    cell row and hence increase downwards, while j represents the cell
    column and hence increases to the right.
    """

    def __init__(self, m, n):
        """
        Initializes a solver for a Sudoku puzzle with block size m×n.

        m: The number of rows per puzzle block.
        n: The number of columns per puzzle block.
        """

        self.m = m
        self.n = n

        N = m * n

        # initialize the Sudoku model
        self.sudoku_model = pulp.LpProblem("Sudoku", pulp.LpMinimize)

        # define the names of all associated ILP problem variables
        x_names = [var_name(i, j, k)
                   for i in crange(1, N)
                   for j in crange(1, N)
                   for k in crange(1, N)]

        # create a dictionary with all the needed variables x_{i,j,k}
        self.x = pulp.LpVariable.dict("%s",
                                      x_names,
                                      lowBound=0,
                                      upBound=1,
                                      cat=pulp.LpInteger)

        # objective function (irrelevant in practice)
        self.sudoku_model += 0

        # constraint: each value k appears exactly once in each row i
        for i in crange(1, N):
            for k in crange(1, N):
                self.sudoku_model += sum([self.x[var_name(i, j, k)]
                                          for j in crange(1, N)]) == 1

        # constraint: each value k appears exactly once in each column j
        for j in crange(1, N):
            for k in crange(1, N):
                self.sudoku_model += sum([self.x[var_name(i, j, k)]
                                          for i in crange(1, N)]) == 1

        # contraint: each value k appears exactly once in each block (I,J)
        for I in crange(1, n):
            for J in crange(1, m):

                i_low = (I - 1) * m + 1
                j_low = (J - 1) * n + 1
                block_i_values = range(i_low, i_low + m)
                block_j_values = range(j_low, j_low + n)

                for k in crange(1, N):
                    self.sudoku_model += sum([self.x[var_name(i, j, k)]
                                              for i in block_i_values
                                              for j in block_j_values]) == 1

        # contraint: each cell (i,j) must have some value k
        for i in crange(1, N):
            for j in crange(1, N):
                self.sudoku_model += sum([self.x[var_name(i, j, k)]
                                          for k in crange(1, N)]) == 1

    def set_cell_value(self, i, j, k):
        """
        Sets the value of cell (i,j) to k.

        This function will throw a RuntimeError exception if called
        after the puzzle has already been solved.
        """

        if self.sudoku_model.status != pulp.LpStatusNotSolved:
            raise RuntimeError("Puzzle has already been solved.")

        self.sudoku_model += self.x[var_name(i, j, k)] == 1

    def get_cell_value(self, i, j):
        """
        Returns the value of cell (i,j) or None if the puzzle has not
        yet been solved.
        """

        N = self.size()

        for k in crange(1, N):
            if self.x[var_name(i, j, k)].value() == 1:
                return k
        return None

    def solve(self):
        """
        Solves the puzzle and returns True if the puzzle is solvable,
        False otherwise.
        """

        status = self.sudoku_model.solve()
        return status == pulp.LpStatusOptimal

    def size(self):
        """Returns the number of rows/columns in the puzzle."""

        return self.m * self.n
