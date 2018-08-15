#!/usr/bin/env python3


class WordTracker(object):
    """
    This class is used to track occurrences of words.
     The class uses a fixed list of words as its dictionary
     (note - 'dictionary' in this context is just a name and does
     not refer to the pythonic concept of dictionaries).
     The class maintains the occurrences of words in its
     dictionary as to be able to report if all dictionary's words
     were encountered.
    """

    def __init__(self, word_list):
        """
        Initiates a new WordTracker instance.
        :param word_list: The instance's dictionary.
        """
        self.__word_list = word_list
        self.__length_dic = len(word_list)
        self.__word_list_sorted = word_list[:]
        self.__word_list_sorted = self.merge_sort(self.__word_list)
        self.__amount_of_repetitions = [0] * len(word_list)

    def merge_sort(self,lst):
        if(len(lst) <= 1):
            return lst
        middle = len(lst)//2
        left = self.merge_sort(lst[:middle])
        right = self.merge_sort(lst[middle:])
        sorted_list = self.merge(left,right)
        return sorted_list

    def merge(self,left,right):
        lst = left + right
        l, r = 0, 0
        for i in range(len(left) + len(right)):
            lval = left[l] if l < len(left) else None
            rval = right[r] if r < len(right) else None
            if (lval and rval and lval < rval) or rval is None:
                lst[i] = lval
                l += 1
            elif (lval and rval and lval >= rval) or lval is None:
                lst[i] = rval

                r += 1
        return lst

    def binary_search(self,sorted_data,item):
        """returns the index of the item in the data,
           if it was found. None otherwise"""
        bottom = 0 #The first cell in the suspected range
        top = len(sorted_data)-1 #the last cell
        while (top>=bottom):
            middle = (top+bottom)//2
            if sorted_data[middle] < item:
                bottom = middle+1
            elif sorted_data[middle] > item:
                top = middle-1
            elif sorted_data[middle] == item:
                return middle
        return None

    def __contains__(self, word):
        """
        Check if the input word in contained within dictionary.
         For a dictionary with n entries, this method guarantees a
         worst-case running time of O(n) by implementing a
         binary-search.
        :param word: The word to be examined if contained in the
        dictionary.
        :return: True if word is contained in the dictionary,
        False otherwise.
        """
        i = self.binary_search(self.__word_list_sorted,word)
        if(i) or (i == 0):
            return True
        else:
            return False

    def encounter(self, word):
        """
        A "report" that the give word was encountered.
        The implementation changes the internal state of the object as
        to "remember" this encounter.
        :param word: The encountered word.
        :return: True if the given word is contained in the dictionary,
        False otherwise.
        """
        i = self.binary_search(self.__word_list_sorted,word)
        if (i) or (i == 0):
        # if a index that was returned by the binary search is 0
        # then without the (i==0) the function will return False
            self.__amount_of_repetitions[i] += 1
            return True
        else:
            return False

    def encountered_all(self):
        """
        Checks whether all the words in the dictionary were
        already "encountered".
        :return: True if for each word in the dictionary,
        the encounter function was called with this word;
        False otherwise.
        """
        for i in self.__amount_of_repetitions:
            if(not i):
                return False
        return True

    def reset(self):
        """
        Changes the internal representation of the instance such
        that it "forget" all past encounters. One implication of
        such forgetfulness is that for encountered_all function
        to return True, all the dictionaries' entries should be
        called with the encounter function (regardless of whether
        they were previously encountered ot not).
        """

        self.__amount_of_repetitions = [0] * self.__length_dic












