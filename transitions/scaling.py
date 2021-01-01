#!/usr/bin/env python3

import time
import domino_tiles_transition_graph_breadth_first as dttgbf

def print_results(timing_results: dict, search_results: dict) -> None:
    for grid_size_tuple, timing in timing_results.items():
        print(grid_size_tuple,":",timing)
    for grid_size_tuple, list_of_transitions in search_results.items():
        print(grid_size_tuple,":\n",len(list_of_transitions),"\n",list_of_transitions[0])


if __name__=="__main__":
    grid_sizes = [(4,4), (5,5), (6,6), (7,7), (8,8), (9,9),(10,10),(11,11)]
    starting_value=1
#    maximum_number_of_lists=1000 # insufficient threshold for (6,6)
#    maximum_number_of_lists=10000 # insufficient threshold for (8,8)
    maximum_number_of_lists=100000 # insufficient threshold for (8,8)

    print_status=False
    timing_results = {}
    search_results = {}

    for grid_size_tuple in grid_sizes:
        width = grid_size_tuple[0]
        height = grid_size_tuple[1]
        number_of_tiles_in_grid=width*height

        transition_dic = dttgbf.create_dict_of_adjacent_tile_indices(width,height)

        list_of_transitions=[]

        start_search_time = time.time()
        list_of_transitions.append([starting_value])
        if print_status:
            print("list of transitions:")
            for this_list in list_of_transitions: print(this_list)

        for loop_indx in range(number_of_tiles_in_grid-1):
            print("\nstep "+str(loop_indx) + " of "+str(number_of_tiles_in_grid)+" for "+str(width)+"x"+str(height))
            list_of_transitions = dttgbf.append_next_value(transition_dic,list_of_transitions,
                                                           maximum_number_of_lists,
                                                           number_of_tiles_in_grid,print_status=False)
            print("number of active searches = "+str(len(list_of_transitions)))
            if len(list_of_transitions)<1:
                print("maximum_number_of_lists too low? Stopping")
                print_results(timing_results, search_results)
                exit()

        timing_results[grid_size_tuple] = time.time()-start_search_time
        search_results[grid_size_tuple] = list_of_transitions
        print("for "+str(width)+"x"+str(height)+", number of successes ="+str(len(list_of_transitions)))

    print_results(timing_results, search_results)
