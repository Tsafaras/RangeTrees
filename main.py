# import sys
# from AVL_Tree import *
from handle_csv import fill_csv, extract_csv
# from AVL_Node import AVL_Node
from time import process_time as pt
# from math import log

# N = int(input("Enter size of N: "))
# while N<1:
#    N = int(input("Enter size of N (greater than zero this time):"))
# fill_csv(N)
tree = extract_csv()
# print(tree) #requires "pretty print tree.txt" code
time = pt()  # time elapsed since start of program
time = pt()-time
# print("Elapsed time is:",time)
# list = tree.range_query()
# for i in list:
#     print(i)