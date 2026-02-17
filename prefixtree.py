#!python3

from prefixtreenode import PrefixTreeNode


class PrefixTree:
    """PrefixTree: A multi-way prefix tree that stores strings with efficient
    methods to insert a string into the tree, check if it contains a matching
    string, and retrieve all strings that start with a given prefix string.
    Time complexity of these methods depends only on the number of strings
    retrieved and their maximum length (size and height of subtree searched),
    but is independent of the number of strings stored in the prefix tree, as
    its height depends only on the length of the longest string stored in it.
    This makes a prefix tree effective for spell-checking and autocompletion.
    Each string is stored as a sequence of characters along a path from the
    tree's root node to a terminal node that marks the end of the string."""

    # Constant for the start character stored in the prefix tree's root node
    START_CHARACTER = ''

    def __init__(self, strings=None):
        """Initialize this prefix tree and insert the given strings, if any."""
        # Create a new root node with the start character
        self.root = PrefixTreeNode(PrefixTree.START_CHARACTER)
        # Count the number of strings inserted into the tree
        self.size = 0
        # Insert each string, if any were given
        if strings is not None:
            for string in strings:
                self.insert(string)

    def __repr__(self):
        """Return a string representation of this prefix tree."""
    # r is for repr, which is the object representation as opposed to the human readable string version 
    # which would be str() !r is just shorthand for repr() and specifically inside f-strings
        return f'PrefixTree({self.strings()!r})'

    def is_empty(self):
        """Return True if this prefix tree is empty (contains no strings)."""
        if self.size == 0:
            return True
        else:
            return False 

    def contains(self, string):
        """Return True if this prefix tree contains the given string."""
        # use _find_node as a helper 
        # use tuple unpacking to set the tuple values to 2 local variables
        node, depth = self._find_node(string)
        # check if the depth (which is all the letters that match) matches len
        # and check if the deepest matching node is also the end of that branch
        if depth == len(string) and node.is_terminal():
            return True
        else:
            return False

    def insert(self, string):
        """Insert the given string into this prefix tree."""
        # first check if the string already exists before increasing size, could be a duplicate string
        # save the result now before we modify anything in the tree
        already_exists = self.contains(string)
        # start at the root node
        node = self.root
        # loop through the string, check if the node has a matching child,
        # if so, reassign node to the value of the child char to force traversal down the tree
        for char in string:
            if node.has_child(char):
                node = node.get_child(char)
        # if char is not a child, create a new child_node by initializing a new PrefixTreedNode
        # then add_child and move to it by reassigning node's value to move down the tree to the newly created node
            else:
                child_node = PrefixTreeNode(char)
                node.add_child(char, child_node)
                node = child_node
        # once the loop finishes, increase self.size by 1 to show that a new word has been added
        # and the loop ends with the final node having been reassigned to node so assign that node as terminal
        node.terminal = True
        if not already_exists:
            self.size += 1
        

    def _find_node(self, string):
        """Return a tuple containing the deepest node in this prefix tree that
        matches the longest prefix of the given string and the node's depth.
        The depth returned is equal to the number of prefix characters matched.
        Search is done iteratively with a loop starting from the root node."""
        # Match the empty string
        if len(string) == 0:
            return self.root, 0
        # Start with  node set to the root node
        node = self.root
        depth = 0
        # loop through each char in the string (there is no way to loop through nodes in a tree
        # bc they aren't linear, they branch)
        for char in string:
        # call has_child to see if the given char is a child of that node
            if node.has_child(char):
        # increase depth counter
                depth += 1
        # reassign node using get_child (which returns back an elemnt) now that element
        # can be used in the next iteration of the loop which forces the nodes to progress
        # down the tree 
                node = node.get_child(char)
            else:
                return node, depth
        # return the tuple of 2 numbers        
        return node, depth

            


    def complete(self, prefix):
        """Return a list of all strings stored in this prefix tree that start
        with the given prefix string."""
        # Create a list of completions in prefix tree
        completions = []
        node, depth = self._find_node(prefix)
        if depth == len(prefix):
            self._traverse(node, prefix, completions.append)
        return completions

    def strings(self):
        """Return a list of all strings stored in this prefix tree."""
        # Create a list of all strings in prefix tree
        all_strings = []
        node = self.root
        prefix = ''
        self._traverse(node, prefix, all_strings.append)
        return all_strings

    def _traverse(self, node, prefix, visit):
        """Traverse this prefix tree with recursive depth-first traversal.
        Start at the given node with the given prefix representing its path in
        this prefix tree and visit each node with the given visit function."""
        # if this node is terminal, we found a complete word so call visit on it
        # visit is a placeholder function passed into _traverse. whatever function calls _traverse will need to provide the defintion
        # of visit within the caller's scope, but traverse doesn't need to see that definition, as it's being given the whole thing by the caller
        # visit will be responsible for recording the completed word that was found and adding it to the completeions []
        if node.is_terminal():
            visit(prefix)
        # the for loop is responsible for recursively traversing each child node, adding its character to the prefix
        # building the string one letter deeper when there is a match progressively making prefix longer until ending the recursive loop when 
        # it finds a node that is terminal (when it passes responsibility to visit to add the found word to list of complete words) OR when it finds a node 
        # that has no children (not always the same as a terminal node) where it ends.
        # use .items to access both key and value pair from the children dict
        for char, child_node in node.children.items():
            self._traverse(child_node, prefix + char, visit)


def create_prefix_tree(strings):
    print(f'strings: {strings}')

    tree = PrefixTree()
    print(f'\ntree: {tree}')
    print(f'root: {tree.root}')
    print(f'strings: {tree.strings()}')

    print('\nInserting strings:')
    for string in strings:
        tree.insert(string)
        print(f'insert({string!r}), size: {tree.size}')

    print(f'\ntree: {tree}')
    print(f'root: {tree.root}')

    print('\nSearching for strings in tree:')
    for string in sorted(set(strings)):
        result = tree.contains(string)
        print(f'contains({string!r}): {result}')

    print('\nSearching for strings not in tree:')
    prefixes = sorted(set(string[:len(string)//2] for string in strings))
    for prefix in prefixes:
        if len(prefix) == 0 or prefix in strings:
            continue
        result = tree.contains(prefix)
        print(f'contains({prefix!r}): {result}')

    print('\nCompleting prefixes in tree:')
    for prefix in prefixes:
        completions = tree.complete(prefix)
        print(f'complete({prefix!r}): {completions}')

    print('\nRetrieving all strings:')
    retrieved_strings = tree.strings()
    print(f'strings: {retrieved_strings}')
    matches = set(retrieved_strings) == set(strings)
    print(f'matches? {matches}')


def main():
    # Simpe test case of string with partial substring overlaps
    strings = ['ABC', 'ABD', 'A', 'XYZ']
    create_prefix_tree(strings)

    # Create a dictionary of tongue-twisters with similar words to test with
    tongue_twisters = {
        'Seashells': 'Shelly sells seashells by the sea shore'.split(),
        # 'Peppers': 'Peter Piper picked a peck of pickled peppers'.split(),
        # 'Woodchuck': ('How much wood would a wood chuck chuck'
        #                ' if a wood chuck could chuck wood').split()
    }
    # Create a prefix tree with the similar words in each tongue-twister
    for name, strings in tongue_twisters.items():
        print(f'{name} tongue-twister:')
        create_prefix_tree(strings)
        if len(tongue_twisters) > 1:
            print('\n' + '='*80 + '\n')


if __name__ == '__main__':
    main()