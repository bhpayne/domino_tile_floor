#!/usr/bin/env python3

__author__ = """Ben Payne (ben.is.located@gmail.com)"""

import matplotlib.pyplot as plt
import numpy
import seaborn as sns

for index in range(4*3):
    #https://stackoverflow.com/questions/339007/how-to-pad-zeroes-to-a-string
    index_padded = str(index+1).zfill(2)
    #print(index_padded)
    ary = numpy.loadtxt(open("4x3_"+index_padded+".csv", "r"), delimiter=",")

    #  https://stackoverflow.com/a/39482402/1164295
    ax = sns.heatmap(ary, annot=True, cbar=False)#, fmt="d")
    fig = ax.get_figure()

    fig.savefig("output__"+str(index)+".png")
    plt.clf()


# rm 4x3.gif; convert -delay 50 output__{0..10}.png -delay 200 output__11.png -loop 0 4x3.gif
