from handle_csv import *


def giveanumber():
    size = int(input("Enter size of N: "))
    while size <= 0:
        size = int(input("Enter size of N (greater than zero this time): "))
    return size

# N = giveanumber()
#fill_csv(20)
tree = extract_csv()

#tree.inorder()

start = timer()
results = tree.range_query()
if not results:
    exit(0)

skyline, dominant_x, dominant_y = [results[0]], [results[0].y], [results[0].x]
not_x, not_y = [], []

for i in results[1:]:
    plt.scatter(i.y, i.x, c='green')
    if i.y <= skyline[-1].y:
        skyline.append(i)
        dominant_x.append(i.y)
        dominant_y.append(i.x)
    else:
        not_x.append(i.y)
        not_x.append(i.x)
        plt.scatter(i.y, i.x, c='red')

end = timer()
time_elapsed = round(end-start, 3)
print("Skyline time:", time_elapsed)
plt.scatter(dominant_x, dominant_y, c='coral')

plt.xlabel('x - axis')
plt.ylabel('y - axis')
plt.title('Skyline Query!')
plt.show()
