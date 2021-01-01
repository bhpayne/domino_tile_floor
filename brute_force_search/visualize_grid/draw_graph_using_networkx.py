#!/usr/bin/env python3

__author__ = """Ben Payne (ben.is.located@gmail.com)"""

import networkx as nx

#G=nx.grid_2d_graph(4,4)  #4x4 grid
G=nx.grid_graph(dim=[5,5])

pos=nx.spring_layout(G,iterations=1000)

nx.draw(G,pos,font_size=8)
#nx.draw(G,pos,node_color='k',node_size=0,with_labels=False)

#plt.savefig("four_grids.png")
plt.show()
