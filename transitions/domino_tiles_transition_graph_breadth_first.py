#!/usr/bin/env python3

"""
for a given starting location in the grid,
enumerate all viable space-filling curves
"""

import random

def create_dict_of_adjacent_tile_indices(width: int, height: int) -> dict:
    """
    there is a grid of size width*height.
    Each location in the grid has an integer index, 1 to width*height

    the "transition dict" contains
        key:   integer index of each tile in the grid
        value: list of adjacent tile indices.
    """
    transition_dic={}
    num_tiles=width*height
#    print("width= "+str(width))
#    print("height= "+str(height))
    for n in range(1,num_tiles+1):
#        print("\nn = "+str(n))
        adjacent_edges_list=[]
#        print("if (n-1)%width !=0, then left exists; value is "+str((n-1)%width))
        if ((n-1)%width != 0):
#            print("left = "+str(n-1))
            adjacent_edges_list.append(n-1) # left
#        print("if n%width !=0, then right exists; value is "+str(n%width))
        if (n%width     != 0):
#            print("right = "+str(n+1))
            adjacent_edges_list.append(n+1) # right
#        print("if n > width, then top exists")
        if (n > width):
#            print("top = "+str(n-width))
            adjacent_edges_list.append(n-width) # top
#        print("if n<=((width*height)-width), then bottom exists; value is "+str(    ((width*height)-width)))
        if (n<=((width*height)-width)):
#            print("bottom = "+str(n+width))
            adjacent_edges_list.append(n+width) # bottom
        transition_dic[n]=adjacent_edges_list
    return transition_dic


def transition_2x3() -> dict:
    """
    A manually specified transition dict
    for comparison with the "create_dict_of_adjacent_tile_indices" above
    """
    transition_dic={}
    transition_dic[1]=[2,4]
    transition_dic[2]=[1,5,3]
    transition_dic[3]=[2,6]
    transition_dic[4]=[1,5]
    transition_dic[5]=[4,2,6]
    transition_dic[6]=[3,5]
    return transition_dic


def append_next_value(transition_dic: dict,list_of_transitions: list,
                      maximum_number_of_lists: int,
                      number_of_tiles_in_grid: int,print_status: bool) -> list:
    """
    for each space-filling curve, increase the length by
    appending adjacent tile indices
    """
    new_transition_list=[]
    for this_list in list_of_transitions:
        if print_status: print("\nthis list = "+str(this_list))
        if (len(this_list)<(number_of_tiles_in_grid)): # if this list isn't "done"
            if print_status: print("last value = " + str(this_list[-1]))
            for next_value in transition_dic[this_list[-1]]:
                if print_status: print("  next value = "+str(next_value))
                if next_value not in this_list: # valid forward move
#                    if (maximum_number_of_lists is None) or len(list_of_transitions)<maximum_number_of_lists:
                    new_list=list(this_list) # https://stackoverflow.com/questions/2612802/how-to-clone-or-copy-a-list
                    new_list.append(next_value)
                    if print_status: print("    adding next value to list; new list is",new_list)
                    new_transition_list.append(new_list)

    if (maximum_number_of_lists is None) or len(list_of_transitions)<maximum_number_of_lists:
        return new_transition_list
    else: # there is a max limit in place and len(list_of_transitions) exceeds that limit
        #return new_transition_list[:maximum_number_of_lists]
        return random.sample(new_transition_list, min(maximum_number_of_lists,len(new_transition_list)))
    return list_of_transitions

if __name__=="__main__":
    width=5
    height=5
    starting_value=1
    maximum_number_of_lists=None

    number_of_tiles_in_grid=width*height

    transition_dic = create_dict_of_adjacent_tile_indices(width,height)
    # print("dict of adjacent tile indices =")
    # for key,value in transition_dic.items():
    #     print("start = "+str(key) +"; neighbors = "+ str(value))


    list_of_transitions=[]

    print_status=False

    with open('transitions_'+str(width)+'x'+str(height)+'_'+str(starting_value)+'.dat','w') as f:
        f.write("loop index, number of tiles to fill, number of transitions\n")

        this_transition=[starting_value]
        list_of_transitions.append(this_transition)
        if print_status:
            print("list of transitions:")
            for this_list in list_of_transitions: print(this_list)

        for loop_indx in range(number_of_tiles_in_grid-1):
            print("\nstep "+str(loop_indx) + " of "+str(number_of_tiles_in_grid))
            list_of_transitions = append_next_value(transition_dic,list_of_transitions,
                                                    maximum_number_of_lists,
                                                    number_of_tiles_in_grid,print_status=False)
            print("number of active searches = "+str(len(list_of_transitions)))
            f.write(str(loop_indx+1)+" "+str(number_of_tiles_in_grid)+" "+
                    str(len(list_of_transitions))+"\n")

        #    print("list of transitions:")
        #    for this_list in list_of_transitions: print(this_list)
        print("list of transitions:")
        for this_list in list_of_transitions: print(this_list)
