# import sys
# from AVL_Tree import *
from handle_csv import fill_csv, extract_csv
# from AVL_Node import AVL_Node
from time import process_time as pt
# from math import log


def giveanumber():
    size = int(input("Enter size of N: "))
    while size <= 0:
        size = int(input("Enter size of N (greater than zero this time): "))
    return size


# N = giveanumber()
# fill_csv(10)
tree = extract_csv()
# print(tree) # requires "pretty print tree.txt" code
time = pt()  # time elapsed since start of program
time = pt()-time
# print("Elapsed time is:",time)
#'''
results = tree.range_query()
for i in results:
    print(i)
#'''