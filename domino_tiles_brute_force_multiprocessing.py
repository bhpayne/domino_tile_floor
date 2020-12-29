#!/usr/bin/env python3

import multiprocessing as mp

import domino_tiles_brute_force as dtbf
import yaml
import time
from random import randint

# Define an output queue
output = mp.Queue()

def print_grid(grid,num_rows):
  for x in range(num_rows+2):
    print(grid[x])

def find_snakes(num_tries,num_successes,output_max, num_rows,num_columns):
    f=open('results.dat','w')
    results_dic={}
    start_time_between_successes = time.time()
    while (num_tries<max_attempts): # search for random space-filling curves in the grid
        num_tries+=1
        start_time_this_iteration = time.time()

        grid=dtbf.create_grid_with_boundaries(num_rows,num_columns)

        start_x,start_y=dtbf.find_starting_location(grid, num_rows, num_columns)
        current_x=start_x
        current_y=start_y
        value=1
        grid[current_x][current_y]=value

        increment_head=True
        change_value_by=1
        while increment_head:
          next_x,next_y,no_remaining_choices=dtbf.find_next_location(grid,current_x,current_y,watch_evolution)
          if no_remaining_choices:
            increment_head=False
            if (watch_evolution):
              print("no remaining locations for head")
          else:
            value+=1
            grid[next_x][next_y]=value
            current_x=next_x
            current_y=next_y
          if (watch_evolution):
            wait = raw_input("    press enter to continue incrementing head")

        if (watch_evolution):
          print("switching to tail exploration")
        current_x=start_x
        current_y=start_y
        value=0
        increment_tail=True
        change_value_by=-1
        while increment_tail:
          next_x,next_y,no_remaining_choices=dtbf.find_next_location(grid,current_x,current_y,watch_evolution)
          if no_remaining_choices:
            increment_tail=False
          else:
            value+=-1
            grid[next_x][next_y]=value
            current_x=next_x
            current_y=next_y
        if (watch_evolution):
          print("no remaining tail locations")

        if (num_tries%1000==0 and not suppress_display):
          print("num_tries="+str(num_tries))

        if (watch_evolution) and (dtbf.are_there_zeros_on_grid(grid,num_rows,num_columns)):
          print("this snake does not fill the grid")
          print("num_tries="+str(num_tries))
          elapsed_time = time.time() - start_time_this_iteration
          print("elapsed time: "+str(elapsed_time)+" seconds")
        if not dtbf.are_there_zeros_on_grid(grid,num_rows,num_columns):
          if (not suppress_display):
            print("space-filling curve found!")
            print_grid(grid,num_rows)
          num_successes+=1
          if (not suppress_display):
            print("number of tries: "+str(num_tries))
            print("number of successes: "+str(num_successes))
          elapsed_time = time.time() - start_time_between_successes
          if (not suppress_display):
            print("elapsed time: "+str(elapsed_time)+" seconds")
#          wait = raw_input("    press enter to continue to next grid attempt")
          start_time_between_successes = time.time()
          results_dic[num_successes]=[elapsed_time, num_tries]
          if (not suppress_display): print("success index: "+str(num_successes)+" took "+str(elapsed_time)+" seconds with "+str(num_tries)+" tries")
          num_tries=0

          if (num_successes==output_max):
            for key,val in results_dic.items():
              print("elapsed time: "+str(val[0]) +" with "+ str(val[1])+" tries")
              f.write(str(val[0]) +" "+ str(val[1])+"\n")
            f.close()
            break

        if (watch_evolution):
          print("grid: ")
          print_grid(grid,num_rows)
          wait = raw_input("    press enter to continue to next grid attempt")
    return

if __name__ == "__main__":
    # user defined variables
    # dimensions of two dimensional grid:
    watch_evolution=False
    suppress_display=True
    output_max=10

    with open('config.yaml', 'r') as file_handle:
        try:
            config = yaml.safe_load(file_handle)
        except yaml.YAMLError as exc:
            print("Error in configuration file:", exc)

    num_columns=config['width']
    num_rows=config['height']
    if ('num_proc' in config.keys()):
        number_of_processes=config['num_proc']
    else:
        number_of_processes=1
    if ('find_optimal_proc' in config.keys()):
        find_optimal_proc = config['find_optimal_proc']
    else:
        find_optimal_proc = False

    # initialize variables
    num_tries=0
    num_successes=0
    max_attempts=1000000

    #if (output_max%number_of_processes != 0):
    #    print("Need to have output_max%number_of_processes be equal to zero")
    #output_max_per_proc = output_max/number_of_processes

    initial_output_max_per_proc = output_max/number_of_processes
    list_of_max=[initial_output_max_per_proc]*number_of_processes
    elem_indx=0
    while (sum(list_of_max)<number_of_processes):
        list_of_max[elem_indx]+=1
        elem_indx += 1
    #print(list_of_max)

    start_time_for_search = time.time()
    processes = [mp.Process(target=find_snakes, args=(num_tries,num_successes,output_max_per_proc, num_rows,num_columns))
                                         for output_max_per_proc in list_of_max]
    for p in processes:  # Run processes
        p.start()

    for p in processes: # Exit the completed processes
        p.join()

    #results = [output.get() for p in processes]     # Get process results from the output queue
    elapsed_time_for_search = time.time() - start_time_for_search
    print("elapsed time for search: "+str(elapsed_time_for_search)+" seconds")
