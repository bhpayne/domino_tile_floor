# domino_tile_floor

Completely cover a 2D grid with 2x1 domino tiles in a self-avoiding walk.

Threshold objective: find a single 200x200 grid that is indistinguishable from random in 24 hours without purchasing additional compute resources.

# Context

A domino-covered grid is like Numbrix, but with the constraint that the number of tiles in the grid must be even such that the grid could be covered by dominos. For example, this constraint excludes grids of size 3x3 and 9x9.

TODO: gif of two headed snake on 8x8 grid

Additionally, any grid that can be covered by dominos is in scope for this project.

Todo: gif of two headed snake on 8x8 grid with a 2x2 corner missing

Why: I'd like to cover my bathroom floor with dominos such that there is a single contiguous sequence. 

# Jargon

* "success" is when a grid is completely covered by a single contiguous sequence
* "failure" is when a grid can only be partially covered

# methods
* brute force
* transition table, breadth first
* transition table, depth first

# Questions

* for a square grid, are there fewer failures when the initial starting location is in the center or a corner?
* for a rectangular grid (e.g., 10x100), are there fewer failures when the initial starting location is in the center, in the middle of one end, or a corner?

# See also

<https://graphthinking.blogspot.com/2016/12/tile-bathroom-floor-with-dominos.html>

<http://www.mathworks.com/matlabcentral/fileexchange/21720-domino-tiles>
