import math
from node import Node
import sys

def ID3(data_set, attribute_metadata, numerical_splits_count, depth):
    '''
    See Textbook for algorithm.
    Make sure to handle unknown values, some suggested approaches were
    given in lecture.
    ========================================================================================================
    Input:  A data_set, attribute_metadata, maximum number of splits to consider for numerical attributes,
	maximum depth to search to (depth = 0 indicates that this node should output a label)
    ========================================================================================================
    Output: The node representing the decision tree learned over the given data set
    ========================================================================================================

    '''
    # Your code here

    n = Node()
    n.mode = mode(data_set)
    label = check_homogenous(data_set)

    if label is not None:
        n.label = label
        return n

    elif depth == 0:
        n.label = mode(data_set)
        return n

    else:
        best, sv = pick_best_attribute(data_set, attribute_metadata, numerical_splits_count)

        if not best:
            n.label = mode(data_set)
            return n

        n.decision_attribute = best
        n.splitting_value = sv
        n.name = attribute_metadata[best]['name']

        #numeric
        if n.splitting_value:
            m = split_on_numerical(data_set, best, n.splitting_value)
            numerical_splits_count[best] = numerical_splits_count[best] - 1
            if not m[0] or not m[1]:
                n.label = mode(data_set)
            else:
                n_small = ID3(m[0], attribute_metadata, numerical_splits_count, depth-1)
                n_big = ID3(m[1], attribute_metadata, numerical_splits_count, depth-1)
                n.children = [n_small, n_big]

        #nominal
        else:
            n.is_nominal = True
            m = split_on_nominal(data_set, best)
            for k,v in m.items():
                if m[k]:
                    n_curr = ID3(m[k], attribute_metadata, numerical_splits_count, depth-1)
                    if n_curr.decision_attribute != n.decision_attribute:
                        n.children[k] = n_curr
        return n

def check_homogenous(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Checks if the output value (index 0) is the same for all examples in the the data_set, if so return that output value, otherwise return None.
    ========================================================================================================
    Output: Return either the homogenous attribute or None
    ========================================================================================================
     '''
    # Your code here

    if len(data_set) == 0:
        return None

    isHomogenous = True
    expected = None
    for row in data_set:
        if expected is None:
            expected = row[0]
        else:
            if row[0] != expected:
                isHomogenous = False
                break

    return data_set[0][0] if isHomogenous else None

# ======== Test Cases =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  None
# data_set = [[0],[1],[None],[0]]
# check_homogenous(data_set) ==  None
# data_set = [[1],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  1

def pick_best_attribute(data_set, attribute_metadata, numerical_splits_count):
    '''
    ========================================================================================================
    Input:  A data_set, attribute_metadata, splits counts for numeric
    ========================================================================================================
    Job:    Find the attribute that maximizes the gain ratio. If attribute is numeric return best split value.
            If nominal, then split value is False.
            If gain ratio of all the attributes is 0, then return False, False
            Only consider numeric splits for which numerical_splits_count is greater than zero
    ========================================================================================================
    Output: best attribute, split value if numeric
    ========================================================================================================
    '''
    # pass

    def keyMax(m):
        if len(m) == 0:
            return False
        maximum = max(m, key=m.get)
        for k,v in m.items():
            if maximum == v:
                return k

    n_row = len(data_set)
    if n_row == 0:
        return False, False

    n_col = len(attribute_metadata)
    step = len(data_set) / 5 + 1
    #step = len(data_set) / 10 + 1
    #step = len(data_set) / 100 + 1
    #step = 1

    col_ratio = {}
    for i in range(1, n_col):
        is_nominal = attribute_metadata[i]['is_nominal']
        if is_nominal:
            col_ratio[i] = gain_ratio_nominal(data_set, i)
        else:
            col_ratio[i] = gain_ratio_numeric(data_set, i, step)[0]

    best = max(col_ratio, key=col_ratio.get)
    sv = False

    while True:
        if numerical_splits_count[best] != 0:
            break
        else:
            del col_ratio[best]
            if len(col_ratio) == 0:
                return False, False
            best = max(col_ratio, key=col_ratio.get)

    is_nominal = attribute_metadata[best]['is_nominal']

    if not is_nominal:
        sv = gain_ratio_numeric(data_set, best, step)[1]

    return best, sv

# # ======== Test Cases =============================
# numerical_splits_count = [20,20]
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "opprundifferential",'is_nominal': False}]
# data_set = [[1, 0.27], [0, 0.42], [0, 0.86], [0, 0.68], [0, 0.04], [1, 0.01], [1, 0.33], [1, 0.42], [0, 0.51], [1, 0.4]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, 0.51)
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "weather",'is_nominal': True}]
# data_set = [[0, 0], [1, 0], [0, 2], [0, 2], [0, 3], [1, 1], [0, 4], [0, 2], [1, 2], [1, 5]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, False)

# Uses gain_ratio_nominal or gain_ratio_numeric to calculate gain ratio.

def mode(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Takes a data_set and finds mode of index 0.
    ========================================================================================================
    Output: mode of index 0.
    ========================================================================================================
    '''
    # Your code here

    if len(data_set) == 0:
        return None

    m = {}

    for row in data_set:
        if row[0] not in m:
            m[row[0]] = 1
        else:
            m[row[0]] += 1

    #sort by count in descending order
    tmp = sorted(m.items(), key=lambda x: x[1], reverse=True)
    #return key of first element
    return tmp[0][0]


# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# mode(data_set) == 1
# data_set = [[0],[1],[0],[0]]
# mode(data_set) == 0

def entropy(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Calculates the entropy of the attribute at the 0th index, the value we want to predict.
    ========================================================================================================
    Output: Returns entropy. See Textbook for formula
    ========================================================================================================
    '''

    n_row = float(len(data_set))
    n_col = len(data_set[0])
    entropy = 0
    for col in range(n_col):
        m = {}
        for row in data_set:
            if row[0] not in m:
                m[row[0]] = 1
            else:
                m[row[0]] += 1
        entr = 0

        for k,v in m.items():
            entr -= math.log(v/n_row, 2) * v / n_row
        entropy += entr
    return entropy

# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[0],[1],[1],[1]]
# entropy(data_set) == 0.811
# data_set = [[0],[0],[1],[1],[0],[1],[1],[0]]
# entropy(data_set) == 1.0
# data_set = [[0],[0],[0],[0],[0],[0],[0],[0]]
# entropy(data_set) == 0


def gain_ratio_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  Subset of data_set, index for a nominal attribute
    ========================================================================================================
    Job:    Finds the gain ratio of a nominal attribute in relation to the variable we are training on.
    ========================================================================================================
    Output: Returns gain_ratio. See https://en.wikipedia.org/wiki/Information_gain_ratio
    ========================================================================================================
    '''
    # Your code here

    n_row = float(len(data_set))

    m = {}
    for row in data_set:
        if row[0] not in m:
            m[row[0]] = 1
        else:
            m[row[0]] += 1
    entr_total = 0
    for k,v in m.items():
        entr_total -= v / n_row * math.log(v / n_row, 2)

    p = {}
    for row in data_set:
        if row[attribute] not in p:
            p[row[attribute]] = 1
        else:
            p[row[attribute]] += 1

    entr = 0
    for k,v in p.items():
        count = float(v)
        ones = float(0)
        for row in data_set:
            if k == row[attribute] and row[0] == 1:
                ones += 1

        if ones != 0 and ones != count:

            curr = count / n_row * ones / count * math.log(ones / count, 2) + (count / n_row) * (1 - ones / count) * math.log(1 - ones / count, 2)
            entr = entr - curr

    info_gain = entr_total - entr

    intr_value = float(0)
    for k,v in p.items():
        count = float(v)
        curr = count / n_row * math.log(count / n_row, 2)
        intr_value = intr_value - curr

    if intr_value == 0:
        return 0

    #return info_gain
    return info_gain / intr_value



# ======== Test case =============================
# data_set, attr = [[1, 2], [1, 0], [1, 0], [0, 2], [0, 2], [0, 0], [1, 3], [0, 4], [0, 3], [1, 1]], 1
# gain_ratio_nominal(data_set,attr) == 0.11470666361703151
# data_set, attr = [[1, 2], [1, 2], [0, 4], [0, 0], [0, 1], [0, 3], [0, 0], [0, 0], [0, 4], [0, 2]], 1
# gain_ratio_nominal(data_set,attr) == 0.2056423328155741
# data_set, attr = [[0, 3], [0, 3], [0, 3], [0, 4], [0, 4], [0, 4], [0, 0], [0, 2], [1, 4], [0, 4]], 1
# gain_ratio_nominal(data_set,attr) == 0.06409559743967516

def gain_ratio_numeric(data_set, attribute, steps):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, and a step size for normalizing the data.
    ========================================================================================================
    Job:    Calculate the gain_ratio_numeric and find the best single threshold value
            The threshold will be used to split examples into two sets
                 those with attribute value GREATER THAN OR EQUAL TO threshold
                 those with attribute value LESS THAN threshold
            Use the equation here: https://en.wikipedia.org/wiki/Information_gain_ratio
            And restrict your search for possible thresholds to examples with array index mod(step) == 0
    ========================================================================================================
    Output: This function returns the gain ratio and threshold value
    ========================================================================================================
    '''

    split_values = []
    n_row = float(len(data_set))

    for i in range(0, int(n_row), steps):
        split_values.append(data_set[i][attribute])

    m = {}
    entr_total = 0
    for row in data_set:
        if row[0] not in m:
            m[row[0]] = 1
        else:
            m[row[0]] += 1
    entr_total = 0
    for k,v in m.items():
        entr_total -= v / n_row * math.log(v / n_row, 2)

    ratios = []

    for s in split_values:
        small = []
        big = []
        for row in data_set:
            if row[attribute] >= s:
                big.append(row)
            else:
                small.append(row)

        entr = 0
        curr = 0

        count_small = float(len(small))
        count_big = float(len(big))

        ones_big = float(0)
        ones_small = float(0)
        for r in big:
            if r[0] == 1:
                ones_big += 1
        for r in small:
            if r[0] == 1:
                ones_small += 1

        if ones_big != 0 and ones_big != count_big:

            curr += count_big / n_row * ones_big / count_big * math.log(ones_big / count_big, 2) + count_big / n_row * (1 - ones_big / count_big) * math.log(1 - ones_big / count_big, 2)

        if ones_small != 0 and ones_small != count_small:
            curr += count_small / n_row * ones_small / count_small * math.log(ones_small / count_small, 2) + count_small / n_row * (1 - ones_small / count_small) * math.log(1 - ones_small / count_small, 2)

        entr = entr - curr

        intr = 0
        info_gain = entr_total - entr
        if count_small != 0:
            intr -= count_small / n_row * math.log(count_small / n_row, 2)
        if count_big != 0:
            intr -= count_big / n_row * math.log(count_big / n_row, 2)


        #ratios.append(info_gain)
        if intr == 0:
            ratios.append(0)
        else:
            ratios.append((entr_total - entr) / intr)

    ratio = max(ratios)
    split = 0
    for r in range(len(ratios)):
        if ratios[r] == ratio:
            split = split_values[r]
            break

    return (ratio, split)


# ======== Test case =============================
# data_set,attr,step = [[0,0.05], [1,0.17], [1,0.64], [0,0.38], [0,0.19], [1,0.68], [1,0.69], [1,0.17], [1,0.4], [0,0.53]], 1, 2
# gain_ratio_numeric(data_set,attr,step) == (0.31918053332474033, 0.64)
# data_set,attr,step = [[1, 0.35], [1, 0.24], [0, 0.67], [0, 0.36], [1, 0.94], [1, 0.4], [1, 0.15], [0, 0.1], [1, 0.61], [1, 0.17]], 1, 4
# gain_ratio_numeric(data_set,attr,step) == (0.11689800358692547, 0.94)
# data_set,attr,step = [[1, 0.1], [0, 0.29], [1, 0.03], [0, 0.47], [1, 0.25], [1, 0.12], [1, 0.67], [1, 0.73], [1, 0.85], [1, 0.25]], 1, 1
# gain_ratio_numeric(data_set,attr,step) == (0.23645279766002802, 0.29)

def split_on_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  subset of data set, the index for a nominal attribute.
    ========================================================================================================
    Job:    Creates a dictionary of all values of the attribute.
    ========================================================================================================
    Output: Dictionary of all values pointing to a list of all the data with that attribute
    ========================================================================================================
    '''
    # Your code here
    m = {}
    for row in data_set:
        if row[attribute] not in m:
            m[row[attribute]] = [row]
        else:
            m[row[attribute]].append(row)
    return m

# ======== Test case =============================
# data_set, attr = [[0, 4], [1, 3], [1, 2], [0, 0], [0, 0], [0, 4], [1, 4], [0, 2], [1, 2], [0, 1]], 1
# split_on_nominal(data_set, attr) == {0: [[0, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3]], 4: [[0, 4], [0, 4], [1, 4]]}
# data_set, attr = [[1, 2], [1, 0], [0, 0], [1, 3], [0, 2], [0, 3], [0, 4], [0, 4], [1, 2], [0, 1]], 1
# split on_nominal(data_set, attr) == {0: [[1, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3], [0, 3]], 4: [[0, 4], [0, 4]]}

def split_on_numerical(data_set, attribute, splitting_value):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, threshold (splitting) value
    ========================================================================================================
    Job:    Splits data_set into a tuple of two lists, the first list contains the examples where the given
	attribute has value less than the splitting value, the second list contains the other examples
    ========================================================================================================
    Output: Tuple of two lists as described above
    ========================================================================================================
    '''
    smaller = []
    bigger = []

    for row in data_set:
        if row[attribute] < splitting_value:
            smaller.append(row)
        else:
            bigger.append(row)

    return (smaller, bigger)
# ======== Test case =============================
# d_set,a,sval = [[1, 0.25], [1, 0.89], [0, 0.93], [0, 0.48], [1, 0.19], [1, 0.49], [0, 0.6], [0, 0.6], [1, 0.34], [1, 0.19]],1,0.48
# split_on_numerical(d_set,a,sval) == ([[1, 0.25], [1, 0.19], [1, 0.34], [1, 0.19]],[[1, 0.89], [0, 0.93], [0, 0.48], [1, 0.49], [0, 0.6], [0, 0.6]])
# d_set,a,sval = [[0, 0.91], [0, 0.84], [1, 0.82], [1, 0.07], [0, 0.82],[0, 0.59], [0, 0.87], [0, 0.17], [1, 0.05], [1, 0.76]],1,0.17
# split_on_numerical(d_set,a,sval) == ([[1, 0.07], [1, 0.05]],[[0, 0.91],[0, 0.84], [1, 0.82], [0, 0.82], [0, 0.59], [0, 0.87], [0, 0.17], [1, 0.76]])
