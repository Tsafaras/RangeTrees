# import sys
# from AVL_Tree import *
from handle_csv import fill_csv, extract_csv
# from AVL_Node import AVL_Node
from time import process_time as pt
# from math import log
from AVL_Node import AVL_Node
import matplotlib.pyplot as plt

def giveanumber():
    size = int(input("Enter size of N: "))
    while size <= 0:
        size = int(input("Enter size of N (greater than zero this time): "))
    return size


# N = giveanumber()
# fill_csv(Ν)
tree = extract_csv()
# print(tree) # requires "pretty print tree.txt" code
time = pt()  # time elapsed since start of program
time = pt()-time
# print("Elapsed time is:",time)
results = tree.range_query()
if not results:
    exit(0)

skyline, dominant_x, dominant_y = [results[0]], [results[0].y], [results[0].x]
not_x, not_y = [], []

print("Range search results:")
print(results[0])
for i in results[1:]:
    print(i)
    if i.y <= skyline[-1].y:
        skyline.append(i)
        dominant_x.append(i.y)
        dominant_y.append(i.x)
    else:
        not_x.append(i.y)
        not_x.append(i.x)
    plt.scatter(i.y, i.x, c='green')

print("Skyline elements:")
for i in skyline:
    print(i)

plt.scatter(dominant_x, dominant_y, c='coral')
# plt.scatter(not_x, not_y, c='lightblue')

# plt.ylim(0, 10)
# plt.xlim(10, 160)

plt.xlabel('x - axis')
plt.ylabel('y - axis')
plt.title('Skyline Query!')
plt.show()
