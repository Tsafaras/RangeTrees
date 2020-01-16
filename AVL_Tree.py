from AVL_Node import *
# from sys import setrecursionlimit
# lim = 10**6
# setrecursionlimit(lim)

class AVL_Tree:
    def __init__(self):
        self.root = None # empty tree
        self.parent = None # parent tree, used for 2nd and 3rd Dimension

    def __str__(self):
        if self.root is None: return '<empty tree>'
        return str(self.root)

    def find(self, k):
        return self.root and self.root.find(k)

    def left_rotate(self, x):
        y = x.right
        y.parent = x.parent
        if y.parent is None:
            self.root = y
            # self.root.second_dim_tree = x.second_dim_tree
            # x.second_dim_tree.parent = self.root
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
        update_height(x)
        update_height(y)

    def right_rotate(self, x):
        y = x.left
        y.parent = x.parent
        if y.parent is None:
            self.root = y
            # self.root.second_dim_tree = x.second_dim_tree
            # x.second_dim_tree.parent = self.root
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
        update_height(x)
        update_height(y)

    def rebalance(self, node):
        while node is not None:
            update_height(node)
            if height(node.left) >= 2 + height(node.right):
                if height(node.left.left) >= height(node.left.right):
                    self.right_rotate(node)
                else:
                    self.left_rotate(node.left)
                    self.right_rotate(node)
            elif height(node.right) >= 2 + height(node.left):
                if height(node.right.right) >= height(node.right.left):
                    self.left_rotate(node)
                else:
                    self.right_rotate(node.right)
                    self.left_rotate(node)
            node = node.parent

    def insert(self, node):
        second_dim_node = AVL_Node(node.y, node.x, node.z)
        # third_dim_node = AVL_Node(node.z, node.y, node.x)
        if self.root is None:
            self.root = node
            if not self.root.second_dim_tree and not self.parent:
                self.root.second_dim_tree = AVL_Tree()
                self.root.second_dim_tree.root = second_dim_node
                self.root.second_dim_tree.parent = self

        else:
            self.root.insert(node, second_dim_node)
            if self.root.second_dim_tree:
                self.root.second_dim_tree.root.insert(second_dim_node)
            self.rebalance(node)
            if self.root.second_dim_tree:
                self.root.second_dim_tree.rebalance(second_dim_node)
        print(node)

    def firstdim(self):
        return self.root.second_dim_tree and not self.parent and not self.root.third_dim_tree

    def secondim(self):
        return self.parent and self.root.third_dim_tree and not self.root.second_dim_tree

    def thirddim(self):
        return self.parent and not self.root.third_dim_tree and not self.root.second_dim_tree

    def delete(self, k):
        node = self.find(k)
        if node is None:
            return None
        if node is self.root:
            pseudoroot = AVL_Node(None, 0)
            pseudoroot.left = self.root
            self.root.parent = pseudoroot
            deleted = self.root.delete()
            self.root = pseudoroot.left
            if self.root is not None:
                self.root.parent = None
        else:
            deleted = node.delete()
        # node.parent is actually the old parent of the node,
        # which is the first potentially out-of-balance node.
        self.rebalance(deleted.parent)

    def range_query(self):  # x1 limit, x2 limit
        if self.root:

            x1 = int(input("Enter first bound for x_dim range query:"))
            x2 = int(input("Enter second bound for x_dim range query:"))
            while x2 == x1:
                x2 = int(input("Bounds are equal. Enter something other than:", x1))

            y1 = int(input("Enter first bound for y_dim range query:"))
            y2 = int(input("Enter second bound for y_dim range query:"))
            while y2 == y1:
                y2 = int(input("Bounds are equal. Enter something other than:", y1))

            if x1 < x2:
                if y1 < y2:
                    results = self.root.range_query(x1, x2, y1, y2)
                else:
                    results = self.root.range_query(x1, x2, y2, y1)
            elif x1 > x2:
                if y1 < y2:
                    results = self.root.range_query(x2, x1, y1, y2)
                else:
                    results = self.root.range_query(x2, x1, y2, y1)
            return results
        else:
            print("Tree is empty! Can't perform a range query")