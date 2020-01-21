import csv
import random
from pandas import read_csv
from AVL_Tree import *
# from AVL_Node import AVL_Node
from time import process_time as pt
from math import log
import matplotlib.pyplot as plt


def fill_csv(N):  # N = number of data
    x_dim = random.sample(range(1, N+1), N)
    y_dim = random.sample(range(1, N+1), N)
    z_dim = random.sample(range(1, N+1), N)
    zipped = zip(x_dim, y_dim, z_dim)
    with open('data-sets/data4.csv', mode='w') as file:
        fields = ['x', 'y', 'z']
        file_write = csv.DictWriter(file, fieldnames=fields)

        file_write.writeheader()
        for x, y, z in zipped:
            file_write.writerow({'x': x, 'y': y, 'z': z})


def extract_csv():
    df = read_csv('data-sets/data.csv')
    tree = AVL_Tree()
    time = pt()
    for x, y, z in zip(df['x'], df['y'], df['z']):
        node = AVL_Node(x, y, z)
        tree.insert(node)
        plt.scatter(x, y, c='blue')
    time = -(time - pt())
    # print("Elapsed time is:",time)
    # print("Time complexity (for N =",N,") is O(logN) =",log(N,2))
    return tree
