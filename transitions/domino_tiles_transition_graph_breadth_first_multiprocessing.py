#!/usr/bin/env python3

# http://sebastianraschka.com/Articles/2014_multiprocessing.html
import multiprocessing as mp

import yaml

# Define an output queue
output = mp.Queue()

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
    return

def transition_2x3():
    transition_dic={}
    transition_dic[1]=[2,4]
    transition_dic[2]=[1,5,3]
    transition_dic[3]=[2,6]
    transition_dic[4]=[1,5]
    transition_dic[5]=[4,2,6]
    transition_dic[6]=[3,5]
    return transition_dic


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

def get_transitions_for_seed(starting_value,print_status,
                             number_of_tiles_to_fill,transition_dic,list_of_transitions):
    f=open('record_'+str(width)+'x'+str(height)+'_'+str(starting_value)+'.dat','w')

    if print_status: print("\nseed:")
    this_transition=[starting_value]
    list_of_transitions.append(this_transition)
    if print_status:
        print("list of transitions:")
        print_list_of_transitions(list_of_transitions)

    for loop_indx in range(number_of_tiles_to_fill-1):
        print("\nstep "+str(loop_indx) + " of "+str(number_of_tiles_to_fill)+" for seed "+str(starting_value))
        list_of_transitions = append_next_value(transition_dic,list_of_transitions,number_of_tiles_to_fill,print_status)
        print("number of searches = "+str(len(list_of_transitions)))
        f.write(str(loop_indx+1)+" "+str(number_of_tiles_to_fill)+" "+str(len(list_of_transitions))+"\n")
#        print("list of transitions:")
#        print_list_of_transitions(list_of_transitions)
#    return list_of_transitions
    f.close()
    output.put(list_of_transitions)


# these values get over-written by the config.yaml values
width=4
height=4
#starting_value=1
number_of_processes=4

try:
    config = yaml.load(file('config.yaml', 'r'))
except yaml.YAMLError, exc:
    print "Error in configuration file:", exc

config=yaml.load(file('config.yaml','r'))
width=config['width']
height=config['height']
number_of_processes=config['num_proc']

number_of_tiles_to_fill=width*height

transition_dic = create_transition_dic(width,height)
#print_transition_dic(transition_dic)


print_status=False

list_of_transitions=[]
processes = [mp.Process(target=get_transitions_for_seed, args=(starting_value,
                                            print_status,number_of_tiles_to_fill,
                                            transition_dic,list_of_transitions))
                                            for starting_value in range(1,number_of_processes+1)]

# Run processes
for p in processes:
    p.start()

# Exit the completed processes
for p in processes:
    p.join()

# Get process results from the output queue
results = [output.get() for p in processes]

print("list of transitions:")
for this_list_of_transitions in results:
    print_list_of_transitions(this_list_of_transitions)
