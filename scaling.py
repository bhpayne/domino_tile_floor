#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy
import seaborn as sns

import domino_tiles_brute_force as dtbf

# https://docs.python.org/3/library/copy.html
import copy
import time
from random import randint

if __name__ == "__main__":
    # user defined variables
    # dimensions of two dimensional grid:
    grid_sizes = [(5,5), (6,6), (7,7), (8,8)]#, (9,9)]
    watch_evolution=False # if True, print every step to screen
    suppress_display=True # if False, print progress indicators and successes
    output_max=4 # number of successful outcomes

    # initialize variables
    num_tries=0
    num_successes=0

    results_dict={}

    for grid_size_tuple in grid_sizes:
        num_rows = grid_size_tuple[0]
        num_columns = grid_size_tuple[1]
        results_dict[grid_size_tuple] = []

        start_time_between_successes = time.time()
        while True: # search for random space-filling curves in the grid
          num_tries+=1
          start_time_this_iteration = time.time()

          grid=dtbf.grid_search(num_rows,num_columns, watch_evolution)

          if (num_tries%1000==0 and not suppress_display): print("num_tries="+str(num_tries))

          if not dtbf.are_there_zeros_on_grid(grid,num_rows,num_columns):
            if (not suppress_display):
                print("space-filling curve found!")
                dtbf.display_grid(grid)
            num_successes+=1
            if (not suppress_display):
                print("number of tries: "+str(num_tries))
                print("number of successes: "+str(num_successes))
            elapsed_time = time.time() - start_time_between_successes
            if (not suppress_display): print("elapsed time: "+str(elapsed_time)+" seconds")
        #    wait = input("    press enter to continue to next grid attempt")
            start_time_between_successes = time.time()
            tup = (elapsed_time, num_tries)
            results_dict[grid_size_tuple].append(tup)
            # progress indicator
            print("success number "+str(num_successes)+" of "+str(output_max)+
                  " for "+str(num_rows)+"x"+str(num_columns)+
                  " found in "+str(elapsed_time)+" seconds after "+str(num_tries)+" tries")
            num_tries=0

            if (num_successes==output_max):
                num_successes=0
                break


    print("for pasting into Jupyter, the same set of result in a cleaner format:")
    print("rows, columns, time to find success result, number of failures")
    with open('results.dat','w') as file_handle:
        file_handle.write("rows, columns, time to find success result, number of failures\n")
        for key,val in results_dict.items():
            for tup in val:
                print(key[0],",",key[1],",",tup[0],",",tup[1])
                file_handle.write(str(key[0])+","+str(key[1])+","+str(tup[0])+","+str(tup[1])+"\n")
