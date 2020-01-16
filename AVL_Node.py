# from sys import setrecursionlimit
# lim = 10**6
# setrecursionlimit(lim)
from AVL_Tree import *

class AVL_Node:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.parent = None
        self.left = None
        self.right = None
        self.successor = None # next greater value
        self.predecessor = None # previous equal or lesser value
        self.second_dim_tree = None # tree for 2nd dim (y_dim), rooted on 1st (x_dim)
        self.third_dim_tree = None # tree for 3rd dim (z_dim), rooted on 2nd (y_dim)

    def __str__(self): # pretty print the node
        if self.second_dim_tree:
            return "{X= " + str(self.x) + ", Y= " + str(self.y) + ", Z= " + str(self.z) + "}"
        # elif self.third_dim_tree:
            # return "{Y= " + str(self.y) +", X= "+ str(self.x) +", Z= "+ str(self.z) +"}"
        else:
            return "{Y= " + str(self.x) + ", X= " + str(self.y) + ", Z= " + str(self.z) + "}"
            # return "{Z= " + str(self.z) +", Y= "+ str(self.y) +", X= "+ str(self.x) +"}"

    def find(self, k, next=False):
        # next is a boolean variable, used for range_query, in case the lower bound isn't found
        if k == self.x:
            return self
        elif k <= self.x:
            if not self.left:
                if next is False:
                    return None
                else:
                    return self
            else:
                return self.left.find(k, next)
        else:
            if not self.right:
                if next is False:
                    return None
                else:
                    return self
            else:
                return self.right.find(k, next)

    def find_max(self): # Finds max value in tree and returns its node
        current = self
        while current.right:
            current = current.right
        return current

    def find_predecessor(self):  # Finds predecessor of a given node
        if self.left:
            return self.left.find_max()

    def insert(self, node, second_dim_node=None):
        # Inserts a node into the subtree rooted at this node
        if node is None:
            return
        if node.x <= self.x:
            if self.left is None:
                self.left = node
                node.parent = self

                node.successor = self
                if self.predecessor:
                    node.predecessor = self.predecessor
                    self.predecessor.successor = node
                self.predecessor = node

                # 2nd dim stuff
                if second_dim_node:
                    from AVL_Tree import AVL_Tree
                    node.second_dim_tree = AVL_Tree()
                    node.second_dim_tree.root = second_dim_node
                    node.second_dim_tree.parent = node
                # end of 2nd dim stuff

            else:
                self.left.insert(node, second_dim_node)
                if second_dim_node:
                    print(self, self.parent, self.left, self.right, second_dim_node)
                    self.left.second_dim_tree.insert(second_dim_node)
        else:
            if self.right is None:
                self.right = node
                node.parent = self

                node.predecessor = self
                if self.successor:
                    node.successor = self.successor
                    self.successor.predecessor = node
                self.successor = node

                # 2nd dim stuff
                if second_dim_node:
                    from AVL_Tree import AVL_Tree
                    node.second_dim_tree = AVL_Tree()
                    node.second_dim_tree.root = second_dim_node
                    node.second_dim_tree.parent = node
                # end of 2nd dim stuff

            else:
                self.right.insert(node, second_dim_node)
                if second_dim_node:
                    self.right.second_dim_tree.insert(second_dim_node)

    def delete(self):
        if self.left is None or self.right is None:
            if self is self.parent.left:
                self.parent.left = self.left or self.right
                if self.parent.left is not None:
                    self.parent.left.parent = self.parent
            else:
                self.parent.right = self.left or self.right
                if self.parent.right is not None:
                    self.parent.right.parent = self.parent
            return self
        else:
            s = self.find_predecessor()
            self.x, s.x = s.x, self.x
            return s.delete()

    def range_query(self, x_lower, x_upper, y_lower, y_upper):  # lower limit, upper limit
        x_head = self.find(x_lower,True)  # x_head of the list
        y_head = x_head.find(y_lower,True)

        results = [x_head]  # list of results, insert first element
        while results[-1].successor and results[-1].successor.x<=x_upper:  # successor of last element exists
            results.append(results[-1].successor)
        return results

    def has_kids(self):
        return self.left or self.right


def height(node):  # height of this node
    if node is None:
        return -1
    else:
        return node.height


def update_height(node):
    node.height = max(height(node.left), height(node.right)) + 1