from AVL_Node import *


class AVL_Tree:
    def __init__(self, root=None, parent=None):
        self.root = root
        self.parent = parent

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
        y.left = x
        x.parent = y
        x.update()
        y.update()
        if y.dimension is 1:
            from copy import deepcopy
            y.higher_dim_tree = deepcopy(x.higher_dim_tree)
            y.higher_dim_tree.parent = y
            x.higher_dim_tree.purge(y, y.find_max())

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
        y.right = x
        x.parent = y
        x.update()
        y.update()
        if y.dimension is 1:
            from copy import deepcopy
            y.higher_dim_tree = deepcopy(x.higher_dim_tree)
            y.higher_dim_tree.parent = y
            x.higher_dim_tree.purge(y.find_min(), y)

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
            higher_dim_node = AVL_Node(node.y, node.x, node.z, 2)
            node.higher_dim_tree = AVL_Tree(higher_dim_node, node)

        if self.root is None:
            self.root = node
        else:
            self.root.insert(node)
            self.balance(node.parent)

    # we want to remove everything from min_node up to value max_node from this tree
    def purge(self, min_node, max_node):
        to_be_removed = purge(min_node, max_node)
        for i in to_be_removed:
            self.delete(i.y)

    def delete(self, k):
        node = self.find(k)
        if node is None:
            return None
        if node is self.root:
            pseudoroot = AVL_Node(0, 0, 0)
            pseudoroot.left = self.root
            self.root.parent = pseudoroot
            deleted = self.root.delete()
            self.root = pseudoroot.left
            if self.root:
                self.root.parent = None
        else:
            deleted = node.delete()
        self.balance(deleted.parent)

    def range_query(self):  # x_low limit, x_high limit
        x_low = 10  # bound("first", "X")
        x_high = 300  # bound("second", "X")
        y_low = 5  # bound("first", "Y")
        y_high = 220  # bound("second", "Y")

        # make sure the bounds are in ascending order
        if x_low > x_high:
            x_low, x_high = x_high, x_low
        if y_low > y_high:
            y_low, y_high = y_high, y_low

        if self.root:
            results = self.root.range_query(x_low, x_high, y_low, y_high)
            if not results:
                print("No element matches both of the range criteria.")
            return results
        else:
            print("Tree is empty! Can't perform a range query")


def bound(which, dim):
    print("Enter", which, "bound for", dim, end=' dim: ')
    i = int(input())
    return i
