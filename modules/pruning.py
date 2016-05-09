from node import Node
from ID3 import *
from operator import xor

# Note, these functions are provided for your reference.  You will not be graded on their behavior,
# so you can implement them as you choose or not implement them at all if you want to use a different
# architecture for pruning.

def reduced_error_pruning(root,training_set,validation_set):
    '''
    take the a node, training set, and validation set and returns the improved node.
    You can implement this as you choose, but the goal is to remove some nodes such that doing so improves validation accuracy.
    NOTE you will probably not need to use the training set for your pruning strategy, but it's passed as an argument in the starter code just in case.
    '''
    # Your code here

    #iterating by dfs, for each subtree, calculate current validation_set vs subtree into a node by mode.

    todo = []
    if not root.label and root.children:
        if root.is_nominal:
            for k,v in root.children.items():
                todo.append(v)
        else:
            todo.append(root.children[0])
            todo.append(root.children[1])

    while todo:
        curr = todo.pop()
        #prune the subtree
        #if not leaf
        accuracy_before = validation_accuracy(root, validation_set)
        accuracy_after = 0

        if not curr.label:
            curr.label = curr.mode
            accuracy_after = validation_accuracy(root, validation_set)

            print("before: {}, after: {}".format(accuracy_before, accuracy_after))

            if accuracy_after < accuracy_before:
                curr.label = None
                if curr.is_nominal:
                    for k,v in curr.children.items():
                        todo.append(v)
                else:
                    todo.append(curr.children[0])
                    todo.append(curr.children[1])

    return root

def validation_accuracy(tree,validation_set):
    '''
    takes a tree and a validation set and returns the accuracy of the set on the given tree
    '''
    # Your code here

    correct = float(0)

    for x in validation_set:
        if tree.classify(x) == x[0]:
            correct += 1

    n_row = float(len(validation_set))

    return correct/n_row
