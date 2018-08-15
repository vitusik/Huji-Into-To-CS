#############################################################
# FILE : ex5.py
# WRITER : Name: Vitaly Frolov Login: vitaly1991 
# EXERCISE : intro2cs ex5
# DESCRIPTION:
# A set of functions that uses the perceptron algorithm
# to create separator and bias and a generalization error
# for a given data and labels
#############################################################


def dot(A, B):
    """
    :param A: list in the length of n that composed from floats
              or integers - its actually a vector
    :param B: list in the length of n that composed from floats
              or integers - its actually a vector
    :return: the dot product of the two vectors
    """
    n = len(A)
    dot_product = 0
    for i in range(n):
        # the computer needs to run on all the indexes of
        # the vectors and multiply them
        # and add them to the dot product
        dot_product += A[i] * B[i]
    return dot_product

def sign(x):
    """
    :param x: can b a number or a mathematical expression
    :return: 1 if x is greater than 0
            -1 if x is smaller than 0
             0 if x is 0
    """
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

def check_w_b(data,labels,w,b):
    """

    :param data: list in the length of m which contains
                 lists in the length of n
    :param labels: list in the length of m that contains
                   the numbers 1 or -1 that corresponds to
                   the list inside data in the i location
    :param w: weight vector in the length of single vector in data
    :param b: bias
    :return: 1 if the weight vector and the bias are good
             separators too the data, which is checked by
             comparing the values of labels in the place i
             and dot product of the weight vector and and data
             in place i
             0 if not
    """
    for i in range(len(data)):
        if(sign(dot(w,data[i])-b) != labels[i]):
            return 0
    return 1

def v_add(data_x,label,w):
    """
    :param data_x: its actually the list in data that is in the x
                   spot
    :param label: is the tag for data_x
    :param w: the weight vector in the length of single vector
              in data
    :return: there is no return, because /i work on the list w
    """
    for i in range(len(w)):
        w[i] += data_x[i]*label
        # the formula for the sum of 2 two vectors

def perceptron(data, labels):
    """
    :param data: list in the length of m which contains
                 lists in the length of n
    :param labels: list in the length of m that contains
                   the numbers 1 or -1 that corresponds to the
                   list inside data in the i location
    :return: a tuple that contains two values w,b
             w is a weight vector in the length of single vector
             in data and b is the bias for the perception algorithm
    """
    m = len(data)
    n = len(data[m-1])
    b = 0
    w = [0] * n
    count = 0
    while(count <= 10 * m):
        #the amount of iterations that allowed is 10 times the
        # length of on single vector in data
        for x in range(m):
            if(sign(dot(w,data[x])-b) != labels[x]):
                v_add(data[x],labels[x],w)
                b -= 1 * labels[x]
        if(check_w_b(data,labels,w,b)):
            # before I begin another iteration
            # I'm checking the separator w and the bias b
            # and if its good then there is no need to continue
            # the while loop
            return (w,b)
        count += 1

    return(None,None)

def generalization_error(data, labels, w, b):
    """

    ::param data: list in the length of m which contains
                  lists in the length of n
    :param labels: list in the length of m that contains
                   the numbers 1 or -1 that corresponds to
                   the list inside data in the i location
    :param w: weight vector in the length of single vector in data
    :param b: bias
    :return: a list which length is the amount of vectors that
             there are in data, which contains 1 which means
             that the weight vector and the bias were wrong
             in the categorization of the vector,
             and 0 which means that the weight vector and the
             bias are good separators for that specific vector
    """
    if (w == None) or ( b == None):
        # before I even begin to calculate the generalization
        # error I need to the check that the input that was given
        # to the function is correct
        return None
    m = len(data)
    a = [0] * len(labels)
    for i in range(m):
        if(sign(dot(w,data[i])-b) == labels[i]):
            a[i] = 0
        else:
            a[i] = 1
    return a

def vector_to_matrix(vec):
    """
    :param vec: vector in unknown length however its length has
                square root which is an integer
    :return: square matrix of this vector, which is actually
             a list of lists
    """
    a = len(vec)
    i = int(a ** 0.5)
    if (i * i < a):
        # if the length of the given vector doesnt have
        # a square root which is an integer the function
        # cannot create a square matrix
        return None
    return [vec[x:x+i] for x in range(0, a, i)]
    # the for loop runs on all the length of the given vector
    # but at each iteration the index goes up by the square root
    # of the length of the vector thus creating
    # a list by the length of the square root of the length
    # which contains lists which equal in length to the original

def classifier_4_7(data, labels):
    """
    this function was created to define a classifier for vectors
    that in 2D presentation represents the number 4 or 7
    :param data: list in the length of m which contains
                 lists in the length of n
    :param labels: list in the length of m that contains
                   the numbers 1 or -1 that corresponds to
                   the list inside data in the i location
    :return: the perceptron function with data and labels
             as its arguments
    """
    return perceptron(data,labels)

def test_4_7(train_data, train_labels, test_data, test_labels):
    """

    :param train_data: list in the length of m which contains
                       lists in the length of n
    :param train_labels: list in the length of m that contains
                         the numbers 1 or -1 that corresponds to
                         the list inside data in the i location
    :param test_data: list in the length of a which contains
                      lists in the length of n
    :param test_labels: list in the length of a that contains
                        the numbers 1 or -1 that corresponds to
                        the list inside data in the i location
    :return: weight vector and bias that were calculated
             using the train_data and labels_data
             and a list that represents the generalization error
             for test_data and label_data
    """
    w,b = classifier_4_7(train_data,train_labels)
    if(generalization_error(test_data,test_labels,w,b)):
        # before I return something I check whether the
        # weight vector and the bias were found in the
        # previous function
        return w,b,generalization_error(test_data,test_labels,w,b)
    else:
        return None,None,None








