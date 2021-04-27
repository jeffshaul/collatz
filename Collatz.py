#!/usr/bin/env python
# coding: utf-8

# In[9]:


import networkx as nx
import matplotlib.pyplot as plt
import math
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


def apply_collatz(n):
    if n % 2 == 0:
        return n // 2
    else:
        return 3*n + 1


# In[3]:


def create_collatz_network(n):
    G = nx.DiGraph()
    for i in range(1, n + 1):
        if i in G:
            continue
        hailstone = i
        while hailstone != 1:
            next_hailstone = apply_collatz(hailstone)
            G.add_edge(hailstone, next_hailstone)
            hailstone = next_hailstone
    return G


# In[4]:


def stopping_time(n, G):
    return len(nx.shortest_path(G, source = n, target = 1))


# In[10]:


def calculate_positions(G):
    pos = {}
    for n in G:
        r = math.floor(math.log(n, 2))
        theta = ((n - 2**r) / 2**r) * 2 * math.pi
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        pos[n] = (x, y)
    return pos


# In[60]:


def calculate_positions_doubling_radii(G):
    pos = {}
    for n in G:
        r = 2**math.floor(math.log(n, 2))
        theta = ((n - r) / r) * 2 * math.pi
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        pos[n] = (x, y)
    return pos


# In[63]:


def calculate_positions_spiral(G):
    pos = {}
    for n in G:
        floor2pow = 2**math.floor(math.log(n, 2))
        r = n
        theta = ((n - floor2pow) / floor2pow) * 2 * math.pi
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        pos[n] = (x, y)
    return pos


# In[70]:


'''Taken from https://stackoverflow.com/questions/29586520/can-one-get-hierarchical-graphs-from-networkx-with-python-3/29597209#29597209'''
import random

    
def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):

    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.  
    Licensed under Creative Commons Attribution-Share Alike 
    
    If the graph is a tree this will return the positions to plot this in a 
    hierarchical layout.
    
    G: the graph (must be a tree)
    
    root: the root node of current branch 
    - if the tree is directed and this is not given, 
      the root will be found and used
    - if the tree is directed and this is given, then 
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given, 
      then a random choice will be used.
    
    width: horizontal space allocated for this branch - avoids overlap with other branches
    
    vert_gap: gap between levels of hierarchy
    
    vert_loc: vertical location of root
    
    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        '''
    
        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)  
        if len(children)!=0:
            dx = width/len(children) 
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap, 
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos

            
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


# In[47]:


n = 15
G = create_collatz_network(n)
plt.figure(figsize=(10, 10))
plt.title("Hailstone Sequences of 2-" + str(n))
node_colors = ['lightblue' if node <= n else 'lightgray' for node in list(G)]
nx.draw_networkx(G, pos = calculate_positions(G), node_color = node_colors)


# In[69]:


n = 1023
G = create_collatz_network(n)
plt.figure(figsize=(100, 100))
plt.title("Hailstone Sequences of 2-" + str(n))
edgelist = []
for edge in G.edges():
    if edge[0] % 2 == 0 and edge[1] % 2 == 0:
        continue
    edgelist.append(edge)
nx.draw_networkx_edges(G, pos = calculate_positions(G), edgelist = edgelist, width = 0.2, arrowstyle = '-')


# In[67]:


n = 1023
G = create_collatz_network(n)
plt.figure(figsize=(100, 100))
plt.title("Hailstone Sequences of 2-" + str(n) + " (Successive Radii Doubling)")
edgelist = []
for edge in G.edges():
    if edge[0] % 2 == 0 and edge[1] % 2 == 0:
        continue
    edgelist.append(edge)
nx.draw_networkx_edges(G, pos = calculate_positions_doubling_radii(G), edgelist = edgelist, width = 1, arrowstyle = '-')


# In[66]:


n = 1023
G = create_collatz_network(n)
plt.figure(figsize=(100, 100))
plt.title("Hailstone Sequences of 2-" + str(n) + " (Spiralized)")
edgelist = []
for edge in G.edges():
    if edge[0] % 2 == 0 and edge[1] % 2 == 0:
        continue
    edgelist.append(edge)
nx.draw_networkx_edges(G, pos = calculate_positions_spiral(G), edgelist = edgelist, width = 1, arrowstyle = '-')


# In[84]:


n = 15
G = create_collatz_network(n)
plt.figure(figsize=(10,10))
plt.title("Hailstone Sequences of 2-" + str(n) + " Visualized as a Tree")
pos = hierarchy_pos(G.reverse(), 1)
node_colors = ['lightblue' if node <= n else 'lightgray' for node in list(G)]
nx.draw_networkx(G, pos = pos, node_color = node_colors)


# In[98]:


n = 10
G = create_collatz_network(n)
plt.figure(figsize=(20,6))
plt.title("Hailstone Sequences of 2-" + str(n) + " Visualized on The Number Line")
pos = {node:(node, 0) for node in G} 
node_colors = ['lightblue' if node <= n else 'lightgray' for node in list(G)]
nx.draw_networkx(G, pos = pos, node_color = node_colors, connectionstyle="arc3,rad=0.5")


# In[ ]:




