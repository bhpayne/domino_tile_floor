#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy
import seaborn as sns

# https://docs.python.org/3/library/copy.html
import copy
import time
from random import randint

"""
keywords:
domino tile dominos tiles matrix random snake worm snakes worms

two headed snake AKA domino tile matrix aka numbrix

after each
complete realization is found, the script PAUSES.  To continue, press any key
When satisfied, CTRL-C to stop.

For a visual example of what this script accomplishes, see the game
http://www.snakegame.net/
The output of this script is a matrix of a size defined by two
parameters, "numrows" by "numcolumns".  A boarder is placed around this
matrix (the "None000" value) by placing the original matrix into a larger
matrix of dimension (numrows+2) by (numcolumns+2).  The purpose behind
this is to allow the user to specify an arbitrary shape other than just
rectangles.

Now that an arbitrarily shaped empty "matrix" is set up, start filling in
the matrix with a sequence of integers such that at the end of the
process the matrix is filled completely.  To start, choose a random
location for 1.  Next, choose randomly a neighboring location to place 2.  Then
place 3 next to 2 in a random location.  Each of this random choices has
a maximum of four possible outcomes (up, down, left, right of the
previous integer) but sometimes the number of choices is less (only up or
down since left and right are occupied by integers.  This restriction of
choices is what makes the code long: the number of choices depends on the
number of open neighboring elements in the matrix.

In the end, the integers can no longer be incremented as there are no more open neighboring
locations.  This is due to either the matrix being filled or the "snake"
of previous integers has "cut itself off."  (There are open (zero-valued)
elements, but they are inaccessible due to previous choices.)  Normally
this realization would then be discarded since it was not filled.
However, the "snake" could possibly grow from the other end (start at 1
and decrement).  Thus this decreases the number of realizations one
discards.

to view previous successfully filled matrices, view
suc(4,:,:)  # where "4" is the realization number of the matrix.
other recorded information includes
num_tries
num_successes
times
"""

def read_grid_from_csv(filename: str) -> list:
    """
    """
    with open(filename, 'r') as file_handle:
        file_content = file_handle.readlines()

    grid=[]
    for line in file_content:
        temp_list = []
        for elem in line.strip().split(","):
            try:
                temp_list.append(int(elem))
            except ValueError:
                temp_list.append(None)
        grid.append(temp_list)
    return grid

def convert_success_csv_to_frames(filename: str) -> None:
    """
    """
    grid=read_grid_from_csv(filename)
    max_val=0
    for row in grid:
        for val in row:
            try:
                if val>max_val: max_val=val
            except TypeError:
                pass
    min_val = 0
    #min_val=min(x for x in grid[0] if x is not None) # https://stackoverflow.com/questions/2295461/list-minimum-in-python-with-none
    for row in grid:
        for val in row:
            try:
                if val<min_val: min_val=val
            except TypeError:
                pass
    #print("max=",max_val,"min=",min_val)

    for threshold_val in range(min_val,max_val+1):
        #print("threshold=",threshold_val)
        new_grid=copy.deepcopy(grid)
        for row_index,row in enumerate(grid):
            for col_index,val in enumerate(row):
                try:
                    if val>threshold_val:
                        new_grid[row_index][col_index]=-5
                except TypeError:
                    new_grid[row_index][col_index]=-5
        with open(filename+"_frame_"+str(threshold_val),'w') as file_handle:
            for row in new_grid:
                str_to_write=""
                for val in row:
                    str_to_write+=str(val)+","
                file_handle.write(str_to_write[:-1]+"\n")

        ary = numpy.loadtxt(open(filename+"_frame_"+str(threshold_val), "r"), delimiter=",")
        ax = sns.heatmap(ary, annot=True, cbar=False)#, fmt="d")
        fig = ax.get_figure()
        fig.savefig("output__"+str(threshold_val)+".png")
        plt.clf()

        # convert -delay 50 output__{0..63}.png -delay 200 output__64.png -loop 0 8x8.gif
    return


def offset_grid(grid:list) -> list:
    """
    Given a grid with a two-headed snake (positive and negative values),
    off-set each value such that only non-negative values are present
    """
    min = 10000
    for row_index in range(1,len(grid)-1):
        for val in grid[row_index][1:len(grid)-1]:
            try:
                if val<min: min=val
            except TypeError:
                pass
    #print("min=",min)

    for row_index in range(1,len(grid)-1):
        #print("row=",row_index)
        for col_index,val in enumerate(grid[row_index][1:len(grid)-1]):
            #print("row",row_index,"col",col_index)
            #display_grid(grid)
            try:
                if val<0:
                    #print("add",abs(min))
                    grid[row_index][col_index+1] += abs(min)
                else:
                    #print("add",abs(min)-1)
                    grid[row_index][col_index+1] += abs(min)-1
            except TypeError:
                pass
#                grid[row_index][col_index+1] = -5


    return grid

def display_grid(grid: list) -> None:
    """
    print grid to screen
    """
    for index in range(len(grid)):
        print(grid[index])

def save_grid_to_file(grid: list) -> None:
    """
    """
    grid=offset_grid(grid)

    current_time = round(time.time()*1000)
    filename = 'success_'+str(len(grid))+"x"+str(len(grid[0]))+"_"+str(current_time)+'.csv'
    with open(filename,'w') as file_handle:
        for index in range(1,len(grid)-1):
            str_to_write=""
            for val in grid[index][1:-1]:
                str_to_write += str(val)+","
            file_handle.write(str_to_write[:-1]+"\n")

    return filename

def create_grid_with_boundaries(num_rows: int,num_columns: int) -> list:
    """
    """
    grid = [[0 for x in range(num_columns+2)] for y in range(num_rows+2)]

    for indx in range(num_columns+2):
        grid[0][indx]=None
    for indx in range(num_columns+2):
        grid[num_rows+1][indx]=None
    for indx in range(num_rows+2):
        grid[indx][0]=None
    for indx in range(num_rows+2):
        grid[indx][num_columns+1]=None

    # the following is a manual insertion of an empty 2x2 region
    #grid[1][1]=None
    #grid[2][1]=None
    #grid[1][2]=None
    #grid[2][2]=None
    return(grid)

def find_starting_location(grid: list, num_rows: int, num_columns: int):
    """
    """
    found_xy=False
    while not found_xy:
        x=randint(1,num_rows)
        y=randint(1,num_columns)
        #print("x="+str(x)+", y="+str(y))
        if (grid[x][y]==0):
            found_xy=True
    return x,y

def find_next_location(grid: list,current_x: int,current_y: int,watch_evolution: bool):
#  print("finding next location")
#         north
#  west  "value"  east
#         south

  west=grid[current_x][current_y-1]
  east=grid[current_x][current_y+1]
  north =grid[current_x-1][current_y]
  south =grid[current_x+1][current_y] # correct
  if (watch_evolution):
    display_grid(grid)
    print("north=              "+str(north))
    print("west="+str(west)+", value="+str(grid[current_x][current_y])+", east="+str(east))
    print("south=           "+str(south))
    print(" ")
  no_remaining_choices=False
  #      0
  #   0  v  0
  #      0
  if ((north==0) and (south==0) and (east==0) and (west==0)):
    coin = randint(0,3)
    if (coin==0):
#      print("4 choices, 0") # south
      next_x=current_x+1
      next_y=current_y
    elif (coin==1):
#      print("4 choices, 1") # north
      next_x=current_x-1
      next_y=current_y
    elif (coin==2):
#      print("4 choices, 2") # east
      next_x=current_x
      next_y=current_y+1
    else: # (coin==3)
#      print("4 choices, 3") # west
      next_x=current_x
      next_y=current_y-1

  #   0  v  0
  #      0
  elif ((south==0) and (east==0) and (west==0)):
    coin = randint(0,2)
    if (coin==0):
#      print("3 choices V, 0") # south
      next_x=current_x+1
      next_y=current_y
    elif (coin==1):
#      print("3 choices V, 1") # east
      next_x=current_x
      next_y=current_y+1
    else: #(coin==2):
#      print("3 choices V, 2") # west
      next_x=current_x
      next_y=current_y-1
  #      0
  #   0  v  0
  elif ((north==0) and (east==0) and (west==0)):
    coin = randint(0,2)
    if (coin==0):
#      print("3 choices ^, 0") # north
      next_x=current_x-1
      next_y=current_y
    elif (coin==1):
#      print("3 choices ^, 1") # east
      next_x=current_x
      next_y=current_y+1
    else: #(coin==2):
#      print("3 choices ^, 2") # west
      next_x=current_x
      next_y=current_y-1
  #      0
  #   0  v
  #      0
  elif ((north==0) and (south==0) and (west==0)):
    coin = randint(0,2)
    if (coin==0):
#      print("3 choices <, 0") # north
      next_x=current_x-1
      next_y=current_y
    elif (coin==1):
#      print("3 choices <, 1") # south
      next_x=current_x+1
      next_y=current_y
    else: #(coin==2):
#      print("3 choices <, 2") # west
      next_x=current_x
      next_y=current_y-1
  #      0
  #      v  0
  #      0
  elif ((north==0) and (south==0) and (east==0)):
    coin = randint(0,2)
    if (coin==0):
#      print("3 choices >, 0") # north
      next_x=current_x-1
      next_y=current_y
    elif (coin==1):
#      print("3 choices >, 1") # south
      next_x=current_x+1
      next_y=current_y
    else: #(coin==2):
#      print("3 choices >, 2") # east
      next_x=current_x
      next_y=current_y+1
  #      0
  #      v
  #      0
  elif ((north==0) and (south==0)):
    coin = randint(0,2)
    if (coin==0):
#      print("2 choices over/under, 0") # north
      next_x=current_x-1
      next_y=current_y
    else: #(coin==1):
#      print("2 choices over/under, 1") # south
      next_x=current_x+1
      next_y=current_y
  #   0  v  0
  elif ((east==0) and (west==0)):
    coin = randint(0,2)
    if (coin==0):
#      print("2 choices side-by-side, 0") # east
      next_x=current_x
      next_y=current_y+1
    else: #(coin==1):
#      print("2 choices side-by-side, 1") # west
      next_x=current_x
      next_y=current_y-1
  #      0
  #   0  v
  elif ((north==0) and (west==0)):
    coin = randint(0,2)
    if (coin==0):
#      print("2 choices upper-left, 0") # north
      next_x=current_x-1
      next_y=current_y
    else: #(coin==1):
#      print("2 choices upper-left, 1") # west
      next_x=current_x
      next_y=current_y-1
  #      0
  #      v  0
  elif ((north==0) and (east==0)):
    coin = randint(0,2)
    if (coin==0):
#      print("2 choices upper-right, 0") # north
      next_x=current_x-1
      next_y=current_y
    else: #(coin==1):
#      print("2 choices upper-right, 1") # east
      next_x=current_x
      next_y=current_y+1
  #   0  v
  #      0
  elif ((south==0) and (west==0)):
    coin = randint(0,2)
    if (coin==0):
#      print("2 choices lower-left, 0") # south
      next_x=current_x+1
      next_y=current_y
    else: #(coin==1):
#      print("2 choices lower-left, 1") # west
      next_x=current_x
      next_y=current_y-1
  #      v  0
  #      0
  elif ((south==0) and (east==0)):
    coin = randint(0,2)
    if (coin==0):
#      print("2 choices lower-right, 0") # south
      next_x=current_x+1
      next_y=current_y
    else: #(coin==1):
#      print("2 choices lower-right, 1") # east
      next_x=current_x
      next_y=current_y+1
  elif (north==0):
#    print("1 choice, north") # north
    next_x=current_x-1
    next_y=current_y
  elif (south==0):
#    print("1 choice, south") # south
    next_x=current_x+1
    next_y=current_y
  elif (east==0):
#    print("1 choice, east") # east
    next_x=current_x
    next_y=current_y+1
  elif (west==0):
#    print("1 choice, west") # west
    next_x=current_x
    next_y=current_y-1
  else:
    no_remaining_choices=True
    next_x=-1
    next_y=-1

  return next_x,next_y,no_remaining_choices

def are_there_zeros_on_grid(grid: list,num_rows: int,num_columns: int) -> bool:
    """
    """
    for indx in range(num_columns+2):
        for jndx in range(num_rows+2):
            if (grid[jndx][indx]==0):
                return True
    return False


def grid_search(num_rows: int,num_columns: int, watch_evolution:bool) -> list:
    """
    """
    grid=create_grid_with_boundaries(num_rows,num_columns)

    start_x,start_y=find_starting_location(grid, num_rows, num_columns)
    current_x=start_x
    current_y=start_y
    value=1
    grid[current_x][current_y]=value

    increment_head=True
    change_value_by=1
    while increment_head:
        next_x,next_y,no_remaining_choices=find_next_location(grid,current_x,current_y,watch_evolution)
        if no_remaining_choices:
            increment_head=False
            if (watch_evolution): print("no remaining locations for head")
        else:
            value+=1
            grid[next_x][next_y]=value
            current_x=next_x
            current_y=next_y
        if (watch_evolution): wait = input("    press enter to continue incrementing head")

    if (watch_evolution): print("switching to tail exploration")
    current_x=start_x
    current_y=start_y
    value=0
    increment_tail=True
    change_value_by=-1
    while increment_tail:
        next_x,next_y,no_remaining_choices=find_next_location(grid,current_x,current_y,watch_evolution)
        if no_remaining_choices:
            increment_tail=False
        else:
            value+=-1
            grid[next_x][next_y]=value
            current_x=next_x
            current_y=next_y
    if (watch_evolution): print("no remaining tail locations")
    return grid


if __name__ == "__main__":
    # user defined variables
    # dimensions of two dimensional grid:
    num_rows = 8 # grid size
    num_columns = 8 # grid size
    watch_evolution=False # if True, print every step to screen
    suppress_display=False#True # if False, print progress indicators and successes
    create_frames=False
    output_max=1 # number of successful outcomes

    print('for a '+str(num_rows)+"x"+str(num_columns)+" grid, find "+str(output_max)+" successes")

    # initialize variables
    num_tries=0
    num_successes=0

    results_dic={}

    start_time_between_successes = time.time()
    while True: # search for random space-filling curves in the grid
      num_tries+=1
      start_time_this_iteration = time.time()

      grid=grid_search(num_rows,num_columns, watch_evolution)

      if (num_tries%1000==0 and not suppress_display): print("num_tries="+str(num_tries))

      if (watch_evolution) and (are_there_zeros_on_grid(grid,num_rows,num_columns)):
          print("this snake does not fill the grid")
          print("num_tries="+str(num_tries))
          elapsed_time = time.time() - start_time_this_iteration
          print("elapsed time: "+str(elapsed_time)+" seconds")
      if not are_there_zeros_on_grid(grid,num_rows,num_columns):
        if (not suppress_display):
            print("space-filling curve found!")
            display_grid(grid)
            if create_frames:
                filename = save_grid_to_file(grid)
                convert_success_csv_to_frames(filename)
        num_successes+=1
        if (not suppress_display):
            print("number of tries: "+str(num_tries))
            print("number of successes: "+str(num_successes))
        elapsed_time = time.time() - start_time_between_successes
        if (not suppress_display): print("elapsed time: "+str(elapsed_time)+" seconds")
    #    wait = input("    press enter to continue to next grid attempt")
        start_time_between_successes = time.time()
        results_dic[num_successes]=[elapsed_time, num_tries]
        # progress indicator
        print("success number "+str(num_successes)+" of "+str(output_max)+
              " found in "+str(elapsed_time)+" seconds after "+str(num_tries)+" tries")
        num_tries=0

        if (num_successes==output_max):
            break

      if (watch_evolution):
          print("grid: ")
          display_grid(grid)
          wait = input("    press enter to continue to next grid attempt")


    print("for pasting into Jupyter, the same set of result in a cleaner format:")
    print("time to find success result, number of failures")
    with open('results.dat','w') as file_handle:
        for key,val in results_dic.items():
            print(str(val[0]) +", "+ str(val[1]))
            file_handle.write(str(val[0]) +", "+ str(val[1])+"\n")
