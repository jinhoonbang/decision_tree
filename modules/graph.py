from random import shuffle
from ID3 import *
from operator import xor
from parse import parse
import matplotlib.pyplot as plt
import os.path
from pruning import validation_accuracy

# NOTE: these functions are just for your reference, you will NOT be graded on their output
# so you can feel free to implement them as you choose, or not implement them at all if you want
# to use an entirely different method for graphing

def get_graph_accuracy_partial(train_set, attribute_metadata, validate_set, numerical_splits_count, pct, depth):
    '''
    get_graph_accuracy_partial - Given a training set, attribute metadata, validation set, numerical splits count, and percentage,
    this function will return the validation accuracy of a specified (percentage) portion of the trainging setself.
    '''

    train_set.shuffle()
    frac = int(float(pct) / 100 * len(train_set))
    curr_set = train_set[:frac]
    root = ID3(curr_set, attribute_metadata, numerical_splits_count, depth)
    accuracy = validation_accuracy(root, validate_set)

    return accuracy

def get_graph_data(train_set, attribute_metadata, validate_set, numerical_splits_count, iterations, pcts, depth):
    '''
    Given a training set, attribute metadata, validation set, numerical splits count, iterations, and percentages,
    this function will return an array of the averaged graph accuracy partials based off the number of iterations.
    '''

    if i == 0:
        return None

    sum_accuracy = float(0)
    for i in range(iterations):
        sum_accuracy += get_graph_accuracy_partial(train_set, attribute_metadata, validate_set, numerical_splits_count, pct, depth)

    return sum_accuracy / iterations


# get_graph will plot the points of the results from get_graph_data and return a graph
def get_graph(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, iterations, lower, upper, increment):
    '''
    get_graph - Given a training set, attribute metadata, validation set, numerical splits count, depth, iterations, lower(range),
    upper(range), and increment, this function will graph the results from get_graph_data in reference to the drange
    percentages of the data.
    '''
    m = {}
    for i in range(lower, upper, increment):
        accuracy = get_graph_data(train_set, attribute_metadata, validate_set, numerical_splits_count, iterations, i, depth)
        if accuracy:
            m[i] = accuracy

    m[upper] = validation_accuracy(ID3(train_set, attribute_metadata, numerical_splits_count, depth), validation_set)



