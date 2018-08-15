# FILE : ex7.py
# WRITER : Name: Vitaly Frolov Login: vitaly1991
# EXERCISE : intro2cs ex7 2014-2015
# DESCRIPTION:
# A list of functions that enables the user to morph images


from SolveLinear3 import solve_linear_3


def is_point_inside_triangle(point, v1, v2, v3):
    """
    a function that checks if a given point is inside a triangle
    that is formed from v1,v2,v3
    :param point: tuple that contains 2 numbers
    :param v1: tuple that contains 2 numbers
    :param v2: tuple that contains 2 numbers
    :param v3: tuple that contains 2 numbers
    :return: tuple that contains boolean expression which will be true
             if the given point is inside the triangle ,and a solution to
             system of linear equations with 3 variables
    """
    v1x = v1[0]
    v1y = v1[1]
    v2x = v2[0]
    v2y = v2[1]
    v3x = v3[0]
    v3y = v3[1]
    px = point[0]
    py = point[1]
    x = [v1x, v2x, v3x]
    y = [v1y, v2y, v3y]
    coefficient_list = [x, y, [1, 1, 1]]
    right_hand_list = [px, py, 1]
    solution = solve_linear_3(coefficient_list, right_hand_list)
    if (solution[0] < 0) or (solution[1] < 0) or (solution[2] < 0):
        # if either of the variables is smaller than 0 its means the point
        # isn't inside the triangle
        return False, solution
    else:
        return True, solution


def create_base_triangles(list_of_points):
    """
    function that creates the first two triangles that are formed from the
    coordinates of the edges
    :param list_of_points: list of coordinates
    :return: list that contains two tuples, each tuple contains 3 tuples
             that are the x,y coordinate of the triangle edge
    """
    l = []
    a = ((list_of_points[0]), (list_of_points[1]), (list_of_points[2]))
    l.append(a)
    a = ((list_of_points[0]), (list_of_points[3]), (list_of_points[2]))
    l.append(a)
    return l


def create_triangles(list_of_points):
    """

    :param list_of_points: list of coordinates
    :return: list that contains 2 tuples, in case that the list of points
             contains more than 4 points the function will return more
             than 2 tuples, each tuple contains 3 tuples
             that are the x,y coordinate of the triangle edge
    """
    l = create_base_triangles(list_of_points)
    for i in range(4, len(list_of_points)):
        found = False
        j = 0
        while (j <= len(l)) and (not found):
            sol = is_point_inside_triangle(list_of_points[i], l[j][0], l[j][1], l[j][2])
            if sol[0]:
                temp = l[j]
                l.pop(j)
                # the triangle needs to be removed because it contains
                # a coordinate which means the triangle can be divided
                # into 3 smaller triangles
                l.insert(j, tuple(([temp[0], list_of_points[i], temp[1]])))
                l.insert(j+1, tuple(([temp[0], list_of_points[i], temp[2]])))
                l.insert(j+2, tuple(([temp[1], list_of_points[i], temp[2]])))
                found = True
                # once the function created a set of 3 new triangles
                # we can continue checking the next coordinate
            j += 1

    return l


def do_triangle_lists_match(list_of_points1, list_of_points2):
    """

    :param list_of_points1: list of coordinates of the first image
    :param list_of_points2: list of coordinates of the second image
    :return: true if each point in each list is the same corresponding
             triangle
    """
    if len(list_of_points1) != len(list_of_points2):
        # if the amount of points isn't the same there is no need
        # to check the triangles list
        return False
    triangle_list1 = create_triangles(list_of_points1)
    triangle_list2 = create_triangles(list_of_points2)
    # created two list of triangles
    for i in range(len(list_of_points1)):
        found = False
        j = 0
        while (j <= len(triangle_list1)) and (not found):
            sol1 = is_point_inside_triangle(list_of_points1[i],
                                            triangle_list1[j][0],
                                            triangle_list1[j][1],
                                            triangle_list1[j][2])
            sol2 = is_point_inside_triangle(list_of_points2[i],
                                            triangle_list2[j][0],
                                            triangle_list2[j][1],
                                            triangle_list2[j][2])
            if sol1[0] == sol2[0]:
                # if A point in list1 and B point in list2 and they both
                # either belong or not to their corresponding triangles
                # than they match so we can continue to the next point
                found = True
            else:
                return False
            j += 1
    return True


def get_point_in_segment(p1, p2, alpha):
    """

    :param p1: tuple which contains 2 numbers x,y
    :param p2: tuple which contains 2 numbers x,y
    :param alpha: number between 0 and 1
    :return: tuple which contains 2 numbers x,y
             the x's value is relative to the x's value from p1,p2
             via the alpha
             the same for the y
    """
    vx = float((1 - alpha) * p1[0] + alpha * p2[0])
    vy = float((1 - alpha) * p1[1] + alpha * p2[1])
    return vx, vy


def get_intermediate_triangles(source_triangles_list, target_triangles_list, alpha):
    """

    :param source_triangles_list: list that contains triplets of tuples which
                                  each contains tuples of 2, which are
                                  basically the triangles created from image 1
    :param target_triangles_list: list that contains triplets of tuples which
                                  each contains tuples of 2, which are
                                  basically the triangles created from image 2
    :param alpha: number between 0 and 1
    :return: list that contains triplets of tuples which each contains tuples
             of 2, which are the triangles which coordinates are relative
             to the ones in source_triangles_list and target_triangles_list

    """
    list_inter_tri = []
    for i in range(len(source_triangles_list)):
        inter_tri = []
        for j in range(3):
            xy_source = source_triangles_list[i][j]
            xy_target = target_triangles_list[i][j]
            tri = get_point_in_segment(xy_source, xy_target, alpha)
            inter_tri.append(tri)
        list_inter_tri.append(tuple(inter_tri))
    return list_inter_tri


def get_array_of_matching_points(size, triangles_list, intermediate_triangles_list):
    """

    :param size: tuple that contains the size of the image the first
                 parameter is the x value and the second is the y
    :param triangles_list: list that contains the (x,y) coordinates of each
                           triangle
    :param intermediate_triangles_list: list that contains triplets of tuples
             which each contains tuples of 2, which are the triangles which
             coordinates are relative to the ones created from the source
             image and the ones that created from the target image
    :return: list of lists which size defined by the size parameter, each
             internal list contains tuples, each tuple contains an x,y
             coordinate which is the match to the x,y coordinate of the tuple
             itself within the list of lists
    """

    list_of_matching_points = []
    list_of_matching_points_y_axis = []
    len_list = len(intermediate_triangles_list)
    tri_found = False
    triangle_list_index = 0
    for i in range(size[0]):  # runs on X axis
        for j in range(size[1]):  # runs on Y axis
            while(not tri_found) and (triangle_list_index < len_list):
                check = is_point_inside_triangle((i, j),
                                                 intermediate_triangles_list[triangle_list_index][0],
                                                 intermediate_triangles_list[triangle_list_index][1],
                                                 intermediate_triangles_list[triangle_list_index][2])
                if check[0]:
                    # check[0] will be true when the given point
                    # is inside the given triangle
                    tri_found = True
                    # if a triangle was found there is no need
                    # to continue the while loop
                    a, b, c = check[1]
                    triangle = triangles_list[triangle_list_index]
                    tuple = calculate(triangle, a, b, c)
                    list_of_matching_points_y_axis.append(tuple)
                else:
                    # if the point isn't in the given triangle
                    # the function advances to the next triangle in the list
                    triangle_list_index += 1
            tri_found = False
            triangle_list_index = 0
            # after each iteration of the inner for loop there is a
            # need to reset the index of the triangle list, and the
            # stopping condition
        list_of_matching_points.append(list_of_matching_points_y_axis)
        list_of_matching_points_y_axis = []
    return list_of_matching_points


def calculate(triangle, a, b, c):
    """
    a function that calculates and returns (x,y) values while using the
     x,y values of the triangles edges and a,b,c which are the coefficients
    """
    x = triangle[0][0] * a + triangle[1][0] * b + triangle [2][0] * c
    y = triangle[0][1] * a + triangle[1][1] * b + triangle [2][1] * c
    return x, y


def create_intermediate_image(alpha, size, source_image, target_image,
                              source_triangles_list, target_triangles_list):
    """

    :param alpha: number between 0 and 1
    :param size: tuple that contains the size of the image the first
                 parameter is the x value and the second is the y
    :param source_image: the source image, list of list of tuples, each tuple
                         contains RGB values for each of the pixels of the
                         image
    :param target_image: the target image, list of list of tuples, each tuple
                         contains RGB values for each of the pixels of the
                         image
    :param source_triangles_list: list of triangles created from the source
                                  image
    :param target_triangles_list: list of triangles created from the target
                                  image
    :return: image which is a mash of the source and target images
    """

    image_y_axis = []
    image = []
    inter_tri_list = get_intermediate_triangles(source_triangles_list,
                                                target_triangles_list, alpha)
    l1 = get_array_of_matching_points(size, source_triangles_list,
                                      inter_tri_list)
    l2 = get_array_of_matching_points(size, target_triangles_list,
                                      inter_tri_list)

    for x in range(size[0]):
        for y in range(size[1]):
            source_match_point = l1[x][y]
            target_match_point = l2[x][y]
            x_s = source_match_point[0]
            y_s = source_match_point[1]
            x_t = target_match_point[0]
            y_t = target_match_point[1]
            s_rgb = source_image[x_s, y_s]
            t_rgb = target_image[x_t, y_t]
            red = int((1 - alpha) * s_rgb[0] + alpha * t_rgb[0])
            green = int((1 - alpha) * s_rgb[1] + alpha * t_rgb[1])
            blue = int((1 - alpha) * s_rgb[2] + alpha * t_rgb[2])
            image_y_axis.append((red, green, blue))
        image.append(image_y_axis)
        image_y_axis = []
    return image


def create_sequence_of_images(size, source_image, target_image,
                              source_triangles_list, target_triangles_list, num_frames):
    """

    :param alpha: number between 0 and 1
    :param size: tuple that contains the size of the image the first
                 parameter is the x value and the second is the y
    :param source_image: the source image, list of list of tuples, each tuple
                         contains RGB values for each of the pixels of the
                         image
    :param target_image: the target image, list of list of tuples, each tuple
                         contains RGB values for each of the pixels of the
                         image
    :param source_triangles_list: list of triangles created from the source
                                  image
    :param target_triangles_list: list of triangles created from the target
                                  image
    :param num_frames: amount of images we want to have in end
    :return: list of images that begins with source image and slowly morph
             into the target image
    """
    list_of_images = []
    for i in range(num_frames):
        alpha = float(i / (num_frames - 1))
        list_of_images.append(create_intermediate_image(alpha, size, source_image,
                                                        target_image, source_triangles_list,
                                                        target_triangles_list))
    return list_of_images
