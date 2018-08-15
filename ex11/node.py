from string_task import *

class Node():
    def __init__(self, task, next = None):
        """
        :param task: StringTask type of parameter
        :param next: the next node in the link by default is None
        """
        self.__task = task
        self.__next = next

    def get_priority(self):
        """
        :return: the priority of a given task
        """
        return self.__task.get_priority()

    def set_priority(self, new_priority):
        """
        a method that changes the priority of a given task to
        the new priority
        """
        self.__task.set_priority(new_priority)

    def get_task(self):
        """
        returns the task of the node without the next
        """
        return self.__task

    def get_next(self):
        """
        returns the next link in the node chain
        """
        return self.__next

    def set_next(self,next_node):
        """
        changes the next field of a given node to the
        given next_node
        """
        self.__next = next_node

    def has_next(self):
        """
        function that checks if a given node has a next
        """
        if(not self.get_next()):
            return False
        return True

