from modules.ID3 import *
from modules.parse import *
from modules.pruning import *
from modules.graph import *
from modules.predictions import *

import csv

# DOCUMENATION
# ===========================================
# decision tree driver - takes a dictionary of options and runs the ID3 algorithm.
#   Supports numerical attributes as well as missing attributes. Documentation on the
#   options can be found in README.md

options = {
    'train' : 'data/btrain.csv',
    'validate': 'data/bvalidate.csv',
    'predict': 'data/btest.csv',
    'limit_splits_on_numerical': 10,
    'limit_depth': 20,
    'print_tree': False,
    'print_dnf' : True,
    'prune' : 'data/bvalidate.csv',
    'learning_curve' : {
        'upper_bound' : 100,
        'increment' : 10
    }
}

def decision_tree_driver(train, validate = False, predict = False, prune = False,
    limit_splits_on_numerical = False, limit_depth = False, print_tree = False,
    print_dnf = False, learning_curve = False):

    train_set, attribute_metadata = parse(train, False)
    if limit_splits_on_numerical != False:
        numerical_splits_count = [limit_splits_on_numerical] * len(attribute_metadata)
    else:
        numerical_splits_count = [float("inf")] * len(attribute_metadata)

    if limit_depth != False:
        depth = limit_depth
    else:
        depth = float("inf")

    print "###\n#  Training Tree\n###"

    # call the ID3 classification algorithm with the appropriate options

    tree = ID3(train_set, attribute_metadata, numerical_splits_count, depth)
    print '\n'

    print '###\n#  Validating Before Pruning \n###'
    validate_set, _ = parse(validate, False)
    accuracy = validation_accuracy(tree,validate_set)
    print "Accuracy on validation set: " + str(accuracy)

    # tree1 = ID3(train_set, attribute_metadata, numerical_splits_count, depth)
    # print '###\n#  Validating Before Pruning \n###'
    # accuracy1 = validation_accuracy(tree1,validate_set)
    # print "Accuracy on validation set: " + str(accuracy1)
    print ''

    print '###\n#  Decision Tree as DNF Before Pruning\n###'
    cursor = open('./output/DNF.txt','w+')
    cursor.write(tree.print_dnf_tree())
    cursor.close()
    print 'Decision Tree written to /output/DNF'
    print ''
    print "Unpruned Split Count : {}".format(tree.count_splits())

    # call reduced error pruning using the pruning set
    if prune != False:
        print '###\n#  Pruning\n###'
        pruning_set, _ = parse(prune, False)
        reduced_error_pruning(tree,train_set,pruning_set)
        print ''

    # print tree visually
    if print_tree:
        print '###\n#  Decision Tree\n###'
        cursor = open('./output/tree.txt','w+')
        cursor.write(tree.print_tree())
        cursor.close()
        print 'Decision Tree written to /output/tree'
        print ''

    # print tree in disjunctive normalized form
    if print_dnf:
        print '###\n#  Decision Tree as DNF\n###'
        cursor = open('./output/DNF_prune.txt','w+')
        cursor.write(tree.print_dnf_tree())
        cursor.close()
        print 'Decision Tree written to /output/DNF_prune'
        print ''

    # test tree accuracy on validation set
    if validate != False:
        print '###\n#  Validating\n###'
        accuracy = validation_accuracy(tree,validate_set)
        print "Accuracy on validation set: " + str(accuracy)
        print ''
        print "Pruned Split Count : {}".format(tree.count_splits())

    # generate predictions on the test set
    if predict != False:
        print '###\n#  Generating Predictions on Test Set\n###'
        #create_predictions(tree, predict)

        array = []
        csvfile = open(predict,'rb')
        fileToRead = csv.reader(csvfile, delimiter=' ',quotechar=',')

        # skip first line of data
        fileToRead.next()

        attributes = [
        {
            'name': "winpercent",
            'is_nominal': False
        },
        {
            'name': "oppwinningpercent",
            'is_nominal': False
        },
        {
            'name': "weather",
            'is_nominal': True
        },
        {
            'name': "temperature",
            'is_nominal': False
        },
        {
            'name': "numinjured",
            'is_nominal': False
        },
        {
            'name': "oppnuminjured",
            'is_nominal': False
        },
        {
            'name': "startingpitcher",
            'is_nominal': True
        },
        {
            'name': "oppstartingpitcher",
            'is_nominal': True
        },
        {
            'name': "dayssincegame",
            'is_nominal': False
        },
        {
            'name': "oppdayssincegame",
            'is_nominal': False
        },
        {
            'name': "homeaway",
            'is_nominal': True
        },
        {
            'name': "rundifferential",
            'is_nominal': False
        },
        {
            'name': "opprundifferential",
            'is_nominal': False
        },
        {
            'name': "winner",
            'is_nominal': True
        }]


        default = {}
        for i in range(len(attributes) - 1):

            if attributes[i]['is_nominal']:
                m = {}
                for row in fileToRead:
                    temp = row[0].split(',')
                    if temp[i] != '?':
                        val = int(temp[i])
                        if val not in m:
                            m[val] = 1
                        else:
                            m[val] += 1
                maximum = max(m, key=m.get)
                default[i] = maximum

            else:
                sigma = float(0)
                n_row = 0
                for row in fileToRead:
                    n_row += 1
                    temp = row[0].split(',')
                    if temp[i] != '?':
                        sigma += float(temp[i])
                default[i] = sigma / n_row

            csvfile.seek(0)
            fileToRead.next()


        for row in fileToRead:
            temp =row[0].split(',')

            for i in range(len(temp) - 1):
                if temp[i] == '?':
                    temp[i] = default[i]
                elif attributes[i]['is_nominal']:
                    temp[i] = int(temp[i])
                else:
                    temp[i] = float(temp[i])

            d = collections.deque(temp)
            d.rotate(1)
            array.append(list(d))

        inter = []
        for entry in array:
            winner = tree.classify(entry)
            entry[0] = winner
            inter.append(entry)

        final = []
        for entry in inter:
            tmp = entry[1:]
            tmp.append(entry[0])
            final.append(tmp)

        myfile = open("../PS2.csv", 'w')
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerows(final)

        print ''

    # generate a learning curve using the validation set
    if learning_curve and validate:
        print '###\n#  Generating Learning Curve\n###'

        newtree = ID3(train_set, attribute_metadata, numerical_splits_count, depth)

        iterations = 20 # number of times to test each size
        get_graph(train_set, attribute_metadata, validate_set,
            numerical_splits_count, depth, 5, 0, learning_curve['upper_bound'],
            learning_curve['increment'])
        print ''

tree = decision_tree_driver( **options )
