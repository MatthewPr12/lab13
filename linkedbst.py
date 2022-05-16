"""
File: linkedbst.py
Author: Ken Lambert
"""
# pylint:disable=invalid-name
# pylint:disable=no-self-use
# pylint:disable=no-else-return
# pylint:disable=c-extension-no-member
# pylint:disable=inconsistent-return-statements
# pylint:disable=singleton-comparison
# pylint:disable=too-many-branches

import math
import random
import time
import copy

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node is not None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = []

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    def iterative_search(self, item):
        """
        search for item iteratively
        :param item:
        :return:
        """
        root = self._root
        while root is not None:
            if item > root.data:
                root = root.right
            elif item < root.data:
                root = root.left
            else:
                return True
        return False

    def insert_iter(self, item):
        new_node = BSTNode(item)
        root = self._root
        if self.isEmpty():
            self._root = new_node
        else:
            pointer1 = root
            pointer2 = None
            while pointer1 is not None:
                pointer2 = pointer1
                if item < pointer1.data:
                    pointer1 = pointer1.left
                else:
                    pointer1 = pointer1.right
            if pointer2 is None:
                pointer2 = new_node
            elif item < pointer2.data:
                pointer2.left = new_node
            else:
                pointer2.right = new_node
        self._size += 1

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            """
            helper for addition
            :param node:
            :return:
            """
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if item not in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            """
            helper for delete
            :param top:
            :return:
            """
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while currentNode.right is not None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while currentNode is not None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        """
        Return the height of tree
        :return: int
        """
        if self.isEmpty():
            return 0

        def height1(top):
            """
            Helper function
            :param top:
            :return:
            """
            if top is None:
                return -1
            left_height = height1(top.left)
            right_height = height1(top.right)
            return max(left_height, right_height) + 1

        return height1(self._root)

    def is_balanced(self):
        """
        Return True if tree is balanced
        :return:
        """
        if self.height() < 2 * math.log2(self._size + 1) - 1:
            return True
        return False

    def range_find(self, low, high):
        """
        Returns a list of the items in the tree, where low <= item <= high
        :param low:
        :param high:
        :return:
        """
        lyst = []
        root = self._root

        def find_range(root, low, high):
            """
            helper function
            :param root:
            :param low:
            :param high:
            :return:
            """
            if root is None:
                return
            if low < root.data:
                find_range(root.left, low, high)
            if low <= root.data <= high:
                lyst.append(root.data)
            find_range(root.right, low, high)

        find_range(root, low, high)
        return lyst

    def rebalance(self):
        """
        Rebalances the tree.
        :return:
        """
        head = None
        tail = None

        def treeToDLL(root):
            """
            helper function
            :param root:
            :return:
            """
            nonlocal head, tail
            if root is None:
                return
            treeToDLL(root.left)

            node = root
            if head is None:
                head = node
            else:
                tail.right = node
                node.left = tail
            tail = node

            treeToDLL(root.right)
            return head

        head = treeToDLL(self._root)
        self._root = self.buildBST_from_DLL(head)
        return self

    def mid_of_ddl(self, head):
        """
        helper function to find middle element of a doubly linked list
        :param head:
        :return:
        """
        prev = head
        pointer_1 = head
        pointer_2 = head
        while pointer_2 and pointer_2.right:
            prev = pointer_1
            pointer_1 = pointer_1.right
            pointer_2 = pointer_2.right.right
        if prev:
            prev.right = None
        pointer_1.left = None
        return pointer_1

    def buildBST_from_DLL(self, head):
        """
        helper method to build BST
        :param head:
        :return:
        """
        if head is None:
            return None
        mid = self.mid_of_ddl(head)
        root = BSTNode(mid.data)
        if head == mid:
            return root

        root.left = self.buildBST_from_DLL(head)
        root.right = self.buildBST_from_DLL(mid.right)
        return root

    def get_min(self, root):
        """
        helper method to find minimum element of a tree
        :param root:
        :return:
        """
        while root.left:
            root = root.left
        return root

    def get_max(self, root):
        """
        helper method to find maximum element of a tree
        :param root:
        :return:
        """
        while root.right:
            root = root.right
        return root

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        root = self._root
        if not root:
            return None

        curr = None
        while True:
            if item < root.data:
                curr = root
                root = root.left
            elif item > root.data:
                root = root.right
            else:
                if root.right:
                    curr = self.get_min(root.right)
                break
            if root is None:
                return curr.data if curr is not None else None
        return curr.data if curr is not None else None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        root = self._root
        if not root:
            return None
        curr = None
        while True:
            if item < root.data:
                root = root.left
            elif item > root.data:
                curr = root
                root = root.right
            else:
                if root.left:
                    curr = self.get_max(root.left)
                break
            if root is None:
                return curr.data if curr is not None else None

        return curr.data if curr is not None else None

    def inorder_iter(self):
        stack = []
        res = []
        cur_node = self._root
        while True:
            if cur_node is not None:
                stack.append(cur_node)
                cur_node = cur_node.left
            elif stack:
                cur_node = stack.pop()
                res.append(cur_node)
                cur_node = cur_node.right
            else:
                break
        return res

    def array_to_bst(self, arr):
        if not arr:
            return None

        mid = len(arr) // 2
        root = arr[mid]
        root.left = self.array_to_bst(arr[:mid])
        root.right = self.array_to_bst(arr[mid + 1:])
        return root

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        bt_alphabet = LinkedBST()
        with open(path, 'r', encoding='utf-8') as my_file:
            dictionary_list = my_file.read().splitlines()
            # get 10000 random words from the dictionary
            words = random.sample(dictionary_list, 10000)
            bt_alphabet._root = BSTNode(dictionary_list[0])
            bt_alphabet._size += 1
            root = bt_alphabet._root
            random_dictionary = copy.deepcopy(dictionary_list)
            random.shuffle(random_dictionary)
            for i in dictionary_list[1:]:
                root.right = BSTNode(i)
                root = root.right
                bt_alphabet._size += 1

                # bt_alphabet.insert_iter(i)
            bt_random = LinkedBST()
            for i in random_dictionary:
                bt_random.insert_iter(i)

        start_list = time.time()
        for i in words:
            if i in dictionary_list:
                something = True
            else:
                something = False
        end_list = time.time()
        list_duration = end_list - start_list
        print(f"List: {list_duration}")

        start_bt_alphabet = time.time()
        for i in words:
            if bt_alphabet.iterative_search(i):
                something = True
            else:
                something = False
        end_bt_alphabet = time.time()
        bt_alphabet_duration = end_bt_alphabet - start_bt_alphabet
        print(f"Binary tree(alphabetically): {bt_alphabet_duration}")

        start_bt_random = time.time()
        for i in words:
            if bt_random.iterative_search(i):
                something = True
            else:
                something = False
        end_bt_random = time.time()
        bt_random_duration = end_bt_random - start_bt_random
        print(f"Binary tree(randomly): {bt_random_duration}")
        bt_random_rebalanced = bt_random.rebalance()

        start_bt_random_rebalanced = time.time()
        for i in words:
            if bt_random_rebalanced.iterative_search(i):
                something = True
            else:
                something = False
        end_bt_random_rebalanced = time.time()
        bt_random_rebalanced_duration = end_bt_random_rebalanced - start_bt_random_rebalanced
        print(f"Binary Balanced tree(randomly): {bt_random_rebalanced_duration}")


if __name__ == "__main__":
    lbst_demo = LinkedBST()
    lbst_demo.insert_iter('d')
    lbst_demo.insert_iter('b')
    lbst_demo.insert_iter('c')
    lbst_demo.insert_iter('a')
    lbst_demo.insert_iter('e')
    lbst_demo.insert_iter('f')
    lbst_demo.insert_iter('g')
    lbst_demo.insert_iter('h')
    print(lbst_demo)
    # res = lbst_demo.inorder_iter()
    # print([i.data for i in res])
    # new_bst = LinkedBST().array_to_bst(res)
    # new_new = LinkedBST()
    # new_new._root = new_bst
    # print(new_new)

    lbst_demo.demo_bst('words.txt')
    # print(lbst_demo)
    # lbst = LinkedBST()
    # lbst.add(4)
    # lbst.add(2)
    # lbst.add(7)
    # lbst.add(3)
    # lbst.add(6)
    # lbst.add(1)
    # lbst.add(9)
    # lbst1 = LinkedBST()
    # lbst1.add(1)
    # lbst1.add(2)
    # lbst1.add(3)
    # lbst1.add(4)
    # lbst1.add(5)
    # lbst1.add(6)
    # lbst1.add(7)
    # lbst1.add(8)
    #
    # print(lbst)
    # print(lbst.height())
    # print(lbst.is_balanced())
    # print(lbst1)
    # print(lbst1.is_balanced())
    # print(lbst1.rebalance())
    # # print(lbst.successor(5).data)
    # # print(lbst.predecessor(5).data)
    # # print(lbst.successor(14).data)
    # print(lbst.range_find(3, 7))
