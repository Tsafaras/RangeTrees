import csv
import random
from pandas import read_csv
from AVL_Tree import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from timeit import default_timer as timer
my_csv = 'data-sets/data.csv'


def giveanumber():
    size = int(input("Enter size of N: "))
    while size <= 0:
        size = int(input("Enter size of N (greater than zero this time): "))
    return size


def fill_csv(N):  # N = number of data
    x_dim = random.sample(range(1, N+1), N)
    y_dim = random.sample(range(1, N+1), N)
    z_dim = random.sample(range(1, N+1), N)
    zipped = zip(x_dim, y_dim, z_dim)
    with open(my_csv, mode='w') as file:
        fields = ['x', 'y', 'z']
        file_write = csv.DictWriter(file, fieldnames=fields)

        file_write.writeheader()
        for x, y, z in zipped:
            file_write.writerow({'x': x, 'y': y, 'z': z})


# N = giveanumber()
# fill_csv(300)

# --- Create 3D Scatter plot ---
fig = plt.figure()
ax = Axes3D(fig)
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
ax.set_title('Skyline Query!')

# -- Read csv ---
df = read_csv(my_csv)

# --- Build Tree ---
start = timer()

tree = AVL_Tree()
for x, y, z in zip(df['x'], df['y'], df['z']):
    node = AVL_Node(x, y, z)
    tree.insert(node)
    ax.scatter(x, y, z, c='blue')
tree.fill_higher_dim()

end = timer()
time_elapsed = round(end - start, 3)
print("build time:", time_elapsed)


# --- Perform Range and Skyline Query ---
start = timer()
results, skyline = tree.range_query()
if not results:
    exit(0)

dominant_x, dominant_y, dominant_z = [skyline[0].y], [skyline[0].x], [skyline[0].z]

for i in results:  # results of range_query
    ax.scatter(i.y, i.x, i.z, c='red')

for i in skyline[1:]:  # skyline query candidates
    if i.y <= dominant_x[-1]:
        dominant_x.append(i.y)
        dominant_y.append(i.x)
        dominant_z.append(i.z)
end = timer()
ax.scatter(dominant_x, dominant_y, dominant_z, c='green')

time_elapsed = round(end - start, 3)
print("Skyline time:", time_elapsed)

plt.show()
