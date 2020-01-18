from AVL_Node import *


class AVL_Tree:
    def __init__(self):
        self.root = None  # empty tree
        self.parent = None

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
        update_height(x)
        update_height(y)

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
        update_height(x)
        update_height(y)

    def rebalance(self, node):
        while node:
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
        if node.dimension is 1:
            second_dim_node = AVL_Node(node.y, node.x, node.z, 2)
            node.second_dim_tree = AVL_Tree()
            node.second_dim_tree.root = second_dim_node
            node.second_dim_tree.parent = node

        if self.root is None:
            self.root = node

        else:
            self.root.insert(node)

        self.rebalance(node)

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
            if self.root:
                self.root.parent = None
        else:
            deleted = node.delete()
        self.rebalance(deleted.parent)

    def range_query(self, lower=None, upper=None):  # lower limit, upper limit
        if lower is None and upper is None:
            lower = int(input("Enter first bound for range query: "))
            upper = int(input("Enter second bound for range query: "))
        if self.root:
            if lower < upper:
                results = self.root.range_query(lower, upper)
            elif lower > upper:
                results = self.root.range_query(upper, lower)
            else:
                print("Lower limit is equal to upper limit. Enter new numbers to perform a range query")
                lower = int(input("Enter first bound for range query: "))
                upper = int(input("Enter second bound for range query: "))
                results = self.range_query(lower, upper)
            return results
        else:
            print("Tree is empty! Can't perform a range query")