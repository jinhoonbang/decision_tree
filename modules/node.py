# DOCUMENTATION
# =====================================
# Class node attributes:
# ----------------------------
# children - a list of 2 nodes if numeric, and a dictionary (key=attribute value, value=node) if nominal.
#            For numeric, the 0 index holds examples < the splitting_value, the
#            index holds examples >= the splitting value
#
# label - is None if there is a decision attribute, and is the output label (0 or 1 for
#	the homework data set) if there are no other attributes
#       to split on or the data is homogenous
#
# decision_attribute - the index of the decision attribute being split on
#
# is_nominal - is the decision attribute nominal
#
# value - Ignore (not used, output class if any goes in label)
#
# splitting_value - if numeric, where to split
#
# name - name of the attribute being split on

class Node:
    def __init__(self):
        # initialize all attributes
        self.label = None
        self.decision_attribute = None
        self.is_nominal = None
        self.value = None
        self.splitting_value = None
        self.children = {}
        self.name = None
        self.mode = 0

    def classify(self, instance):
        '''
        given a single observation, will return the output of the tree
        '''

       # Your code here
        if self.label is not None:
            #leaf node
            return self.label
        else:
            #tree node
            if self.is_nominal:
                #if tree doesn't know how to classify, return the mode
                if instance[self.decision_attribute] not in self.children:
                    maximum = 0
                    return self.mode
                else:
                #if nominal, recurse on child with matching decision attribute
                    return self.children[instance[self.decision_attribute]].classify(instance)

            else:
                value = instance[self.decision_attribute]
                if value < self.splitting_value:
                    return self.children[0].classify(instance)
                else:
                    return self.children[1].classify(instance)

    def print_tree(self, indent = 0):
        '''
        returns a string of the entire tree in human readable form
        IMPLEMENTING THIS FUNCTION IS OPTIONAL
        '''
        # Your code here
        pass


    def print_dnf_tree(self):
        '''
        returns the disjunct normalized form of the tree.
        '''

        def concat_result(result, condition):
            if not result:
                return " ({}) ".format(condition)
            else:
                return result + "\nv " + "({})".format(condition)

        todo = []
        root = (self, "")
        todo.append(root)
        result = ""

        while todo:
            n = todo.pop()
            # if not leaf node
            node=n[0]
            condition=n[1]

            if node.label is None:
                if node.is_nominal:
                    for k,v in node.children.items():
                        todo.append((v, condition + str(node.name) + " = " + str(k) +" ^"))
                else:
                    todo.append((node.children[0], condition + str(node.name) + " < " + str(node.splitting_value) + " ^"))
                    todo.append((node.children[1], condition + str(node.name) + " >= " + str(node.splitting_value) + " ^"))
            else:
                if node.label == 1:
                    #remove last "^"
                    result = concat_result(result, condition[:-1])
        return result


    def count_splits(self):

        counter = 0
        todo = []
        todo.append(self)

        while todo:
            n = todo.pop()
            if n.label is None:
                counter += 1
                if n.is_nominal:
                    for k,v in n.children.items():
                        todo.append(v)
                else:
                    todo.append(n.children[0])
                    todo.append(n.children[1])

        return counter





















