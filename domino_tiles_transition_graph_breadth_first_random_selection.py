#!/usr/bin/env python3

import random

def create_transition_dic(width,height):
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

def print_transition_dic(transition_dic):
    for key,value in transition_dic.iteritems():
        print("start = "+str(key) +"; neighbors = "+ str(value))


def print_list_of_transitions(list_of_transitions):
    for this_list in list_of_transitions:
        print(this_list)
    return

def append_next_value(transition_dic,list_of_transitions,number_of_tiles_to_fill,print_status):
    new_transition_list=[]
    for this_list in list_of_transitions:
        if print_status: print("\nthis list = ")
        if print_status: print(this_list)
        if (len(this_list)<(number_of_tiles_to_fill)): # if this list isn't "done"
            last_value=this_list[len(this_list)-1]
            if print_status: print("last value = " + str(last_value))
            for next_value in transition_dic[last_value]:
                if print_status: print("next value = "+str(next_value))
                if next_value not in this_list:
                    if print_status: print("adding next value to list")
                    new_list=list(this_list) # https://stackoverflow.com/questions/2612802/how-to-clone-or-copy-a-list
                    new_list.append(next_value)
                    if print_status: print(new_list)
                    new_transition_list.append(new_list)
    list_of_transitions=new_transition_list
    return list_of_transitions

width=7
height=7
starting_value=1
max_to_search=100000
number_of_tiles_to_fill=width*height

transition_dic = create_transition_dic(width,height)
#print_transition_dic(transition_dic)



list_of_transitions=[]

print_status=False

if print_status: print("\nseed:")
this_transition=[starting_value]
list_of_transitions.append(this_transition)
if print_status:
    print("list of transitions:")
    print_list_of_transitions(list_of_transitions)

for loop_indx in range(number_of_tiles_to_fill-1):
    print("\nstep "+str(loop_indx) + " of "+str(number_of_tiles_to_fill))
    list_of_transitions = append_next_value(transition_dic,list_of_transitions,number_of_tiles_to_fill,print_status)
    print("number of searches = "+str(len(list_of_transitions)))
    if (len(list_of_transitions)>max_to_search):
        random.shuffle(list_of_transitions)
        list_of_transitions=random.sample(list_of_transitions, max_to_search)
#    print("list of transitions:")
#    print_list_of_transitions(list_of_transitions)
print("list of transitions:")
print_list_of_transitions(list_of_transitions)

f.close()
