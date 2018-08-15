class WordExtractor(object):
    """
    This class should be used to iterate over words contained in files.
     The class should maintain space complexity of O(1); i.e, regardless
     of the size of the iterated file, the memory requirements ofa class
     instance should be bounded by some constant.
     To comply with the space requirement, the implementation may assume
     that all words and lines in the iterated file are bounded by some
     constant, so it is allowed to read words or lines from the
     iterated file (but not all of them at once).
    """

    def __init__(self, filename):
        """
        Initiate a new WordExtractor instance whose *source file* is
        indicated by filename.
        :param filename: A string representing the path to the instance's
        *source file*
        """
        self.__path = filename
        self.__current_line = 0
        self.__current_word = 0

    def __iter__(self):
        """
        Returns an iterator which iterates over the words in the
        *source file* (i.e - self)
        :return: An iterator which iterates over the words in the
        *source file*
        """
        return self


    def __next__(self):
        """
        Make a single word iteration over the source file.
        :return: A word from the file.
        """
        EOF = ""
        with open(self.__path,"r") as f:
            while(True):
                f.seek(self.__current_line)
                line = f.readline()
                list_of_words = [word for word in line.split()]
                length = len(list_of_words)
                if line == EOF:
                    #checking for end of file
                    raise StopIteration
                elif self.__current_word == length or length == 0:
                    #checking for end of the line
                    self.__current_word = 0
                    self.__current_line = f.tell()
                else:
                    #its means were still in the middle of the line
                    # and can return another word
                    self.__current_word += 1
                    return list_of_words[self.__current_word - 1]








