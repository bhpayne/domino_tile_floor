# domino tile floor

Completely cover a 2D grid with 2x1 domino tiles in a self-avoiding walk.

Threshold objective: find a single 200x200 grid that is indistinguishable from random in 24 hours without purchasing additional compute resources.

# Context

A domino-covered grid is like Numbrix, but with the constraint that the number of tiles in the grid must be even such that the grid could be covered by dominos. For example, this constraint excludes grids of size 3x3 and 9x9.

![gif of two headed snake on 8x8 grid](https://github.com/bhpayne/domino_tile_floor/blob/master/brute_force_search/visualize_grid/8x8.gif?raw=true)

Additionally, any grid that can be covered by dominos is in scope for this project. Below is an image of a square grid with a missing 2x2 patch in the upper left corner.

![gif of two headed snake on 8x8 grid with 2x2 missing](https://github.com/bhpayne/domino_tile_floor/blob/master/brute_force_search/visualize_grid/8x8_missing_2x2.gif?raw=true)

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

<https://oeis.org/search?q=greek+key&sort=&language=&go=Search> and <http://www.njohnston.ca/2009/05/on-maximal-self-avoiding-walks/>
