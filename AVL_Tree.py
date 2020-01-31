from AVL_Node import *


class AVL_Tree:
    def __init__(self, root=None, parent=None):
        self.root = root
        self.parent = parent
        self.leaves_hanging = SortedList()

    def __str__(self):
        if self.root is None:
            return '<empty tree>'
        return str(self.root)

    def find(self, k):
        return self.root and self.root.find(k)

    def left_rotate(self, x):
        y = x.right
        y.parent = x.parent
        if y.parent is None:
            self.root = y
        else:
            if y.parent.left is x:
                y.parent.left = y
            elif y.parent.right is x:
                y.parent.right = y

        x.right = y.left
        if x.right:
            x.right.parent = x
        elif y.dimension is 1:
            x.right_leaf = y.left_leaf
            x.right_leaf.parent = x
            y.left_leaf = None
        y.left = x
        x.parent = y
        x.update()
        y.update()

    def right_rotate(self, x):
        y = x.left
        y.parent = x.parent
        if y.parent is None:
            self.root = y
        else:
            if y.parent.left is x:
                y.parent.left = y
            elif y.parent.right is x:
                y.parent.right = y
        x.left = y.right
        if x.left:
            x.left.parent = x
        elif y.right_leaf:
            x.left_leaf = y.right_leaf
            x.left_leaf.parent = x
            y.right_leaf = None
        y.right = x
        x.parent = y
        x.update()
        y.update()

    def balance(self, node):
        while node:
            node.update()
            if node.balance > 1:
                if node.left.balance > 0:
                    self.right_rotate(node)
                else:
                    self.left_rotate(node.left)
                    self.right_rotate(node)
                return

            elif node.balance < -1:
                if node.right.balance < 0:
                    self.left_rotate(node)
                else:
                    self.right_rotate(node.right)
                    self.left_rotate(node)
                return
            node = node.parent

    def insert(self, node):
        if node.dimension is 1:
            node.higher_dim_tree = AVL_Tree(None, node)
        elif node.dimension is 2:
            node.higher_dim_tree = AVL_Tree(None, node)

        if self.root is None:
            self.root = node
        else:
            self.root.insert(node)
            self.balance(node.parent)

    def range_query(self):  # x_low limit, x_high limit
        x_low = 10  # bound("first", "X")
        x_high = 30  # bound("second", "X")
        y_low = 15  # bound("first", "Y")
        y_high = 40  # bound("second", "Y")
        z_low = 10  # bound("first", "Z")
        z_high = 50  # bound("second", "Z")

        # make sure the bounds are in ascending order
        if x_low > x_high:
            x_low, x_high = x_high, x_low
        if y_low > y_high:
            y_low, y_high = y_high, y_low
        if z_low > z_high:
            z_low, z_high = z_high, z_low

        if self.root:
            results, skyline = self.root.range_query(x_low, x_high, y_low, y_high, z_low, z_high)
            if not results:
                print("No element matches both of the range criteria.")
            return results, skyline
        else:
            print("Tree is empty! Can't perform a range query")

    def fill_higher_dim(self):
        self.root.postorder_traversal()


def bound(which, dim):
    print("Enter", which, "bound for", dim, end=' dim: ')
    i = int(input())
    return i
