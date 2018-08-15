import os
import WordExtractor
import WordTracker

class PathIterator(object):
    """
    An iterator which iterates over all the directories and files
    in a given path (note - in the path only, not in the
    full depth). There is no importance to the order of iteration.
    """
    def __init__(self,file_path):
        self.__path = file_path
        self.__current_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        list_of_dir = os.listdir(self.__path)
        while (True):
            if (self.__current_index == (len(list_of_dir))):
                # the amount of directories is the amount of iterations that
                # can be done
                raise StopIteration
            else:
                self.__current_index += 1
                return os.path.join(self.__path,
                                    list_of_dir[self.__current_index - 1 ])

def path_iterator(path):
    """
    Returns an iterator to the current path's filed and directories.
    Note - the iterator class is not outlined in the original
     version of this file - but rather is should be designed
     and implemented by you.
    :param path: A (relative or an absolute) path to a directory.
    It can be assumed that the path is valid and that indeed it
    leads to a directory (and not to a file).
    :return: An iterator which returns all the files and directories
    in the *current* path (but not in the *full depth* of the path).
    """
    return PathIterator(path)

def print_tree_helper(path, amount_of_indentation, sep = '  '):
    """
    recursive help function
    """
    print(sep * amount_of_indentation ,end="")
    print(os.path.basename(path))
    if (os.path.isdir(path)):
        for files in os.listdir(path):
            print_tree_helper(os.path.join(path,files),
                              amount_of_indentation + 1, sep)

def print_tree(path, sep='  '):
    """
    Print the full hierarchical tree of the given path.
    Recursively print the full depth of the given path such that
    only the files and directory names should be printed (and not
    their full path), each in its own line preceded by a number
    of separators (indicated by the sep parameter) that correlates
    to the hierarchical depth relative to the given path parameter.
    :param path: A (relative or an absolute) path to a directory.
    It can be assumed that the path is valid and that indeed it
    leads to a directory (and not to a file).
    :param sep: A string separator which indicates the depth of
     current hierarchy.
    """
    print_tree_helper(path,0,sep)

def file_with_all_words(path, word_list):
    """
    Find a file in the full depth of the given path which contains
    all the words in word_list.
    Recursively go over  the files in the full depth of the given
    path. For each, check whether it contains all the words in
     word_list and if so return it.
    :param path: A (relative or an absolute) path to a directory.
    In the full path of this directory the search should take place.
    It can be assumed that the path is valid and that indeed it
    leads to a directory (and not to a file).
    :param word_list: A list of words (of strings). The search is for
    a file which contains this list of words.
    :return: The path to a single file which contains all the
    words in word_list if such exists, and None otherwise.
    If there exists more than one file which contains all the
    words in word_list in the full depth of the given path, just one
    of theses should be returned (does not matter which).
    """
    dictionary = WordTracker.WordTracker(word_list)
    path_it = path_iterator(path)
    for i in path_it:
        if (os.path.isfile(i)):
            word_extractor = WordExtractor.WordExtractor(i)
            dictionary.reset()
            for word in word_extractor:
                dictionary.encounter(word)
            if (dictionary.encountered_all()):
                return i
        else:
            file_with_all_words(i,word_list)




