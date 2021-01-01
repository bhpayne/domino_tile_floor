#!/usr/bin/env python3

__author__ = """Ben Payne (ben.is.located@gmail.com)"""

# import matplotlib.pyplot as plt
import numpy
import seaborn as sns

# https://stackoverflow.com/a/4315914/1164295
ary = numpy.loadtxt(open("4x3.csv", "r"), delimiter=",")

#  https://stackoverflow.com/a/39482402/1164295
ax = sns.heatmap(ary, annot=True, cbar=False)#, fmt="d")
fig = ax.get_figure()

fig.savefig("output.png")
