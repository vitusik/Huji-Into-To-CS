class PriorityQueueIterator():

    def __init__(self,queue):
        self.__head = queue.get_head()
        self.__current = self.__head
        if(self.__head == None):
            # if the head is None
            # there is nothing to iterate
            self.__stop = 1
        else:
            self.__stop = 0

    def has_next(self):
        """
        function that checks if the given link in the queue
        has next link, in case there is the function will return True
        otherwise it will return False
        """
        if(not self.__current.get_next()):
            return False
        return True

    def __iter__(self):
        return self

    def __next__(self):
        """
        makes a single iteration over a queue and returns the task
        """
        if (self.__stop):
            raise StopIteration
        if(not self.has_next()):
            self.__stop = 1
        a = self.__current.get_task()
        self.__current = self.__current.get_next()
        return a




