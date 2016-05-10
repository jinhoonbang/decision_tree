import csv, collections

# Note: nominal data are integers while numeric data consists of floats
def parse(filename, keep_unlabeled):
    '''
    takes a filename and returns attribute information and all the data in array of arrays
    This function also rotates the data so that the 0 index is the winner attribute, and returns
    corresponding attribute metadata
    '''
    # initialize variables
    array = []
    csvfile = open(filename,'rb')
    fileToRead = csv.reader(csvfile, delimiter=' ',quotechar=',')

    # skip first line of data
    fileToRead.next()

    # set attributes
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
                temp = row[0].split(',')
                if temp[i] != '?':
                    sigma += float(temp[i])
                    n_row += 1
            default[i] = sigma / n_row

        csvfile.seek(0)
        fileToRead.next()


    # iterate through rows of actual data
    for row in fileToRead:
        # change each line of data into an array
        temp =row[0].split(',')

        if (not keep_unlabeled) and (temp[len(attributes) - 1] == "?"):
            continue
        for i in range(len(temp)):
            # data preprocessing
            if temp[i] == '?':
                temp[i] = default[i]
            elif attributes[i]['is_nominal']:
                temp[i] = int(temp[i])
            else:
                temp[i] = float(temp[i])

        # rotate data so that the target attribute is at index 0
        d = collections.deque(temp)
        d.rotate(1)
        array.append(list(d))

    array.pop()

    # rotate attributes so that it corresponds to the data
    attributes = collections.deque(attributes)
    attributes.rotate(1)
    attributes = list(attributes)

    return array, attributes
