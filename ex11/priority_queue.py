from node import *
from string_task import *
from priority_queue_iterator import *

class PriorityQueue():
    def __init__(self,tasks =[]):
        """
        :param tasks: list of tasks, comes in StringTask type
        initializes the queue with the given tasks
        """
        self.__head = None
        self.__q_length = 0
        for i in tasks:
            # each task is inserted into the queue
            self.enque(i)
        self.__current = self.__head

    def enque(self,task):
        """
        :param task: task from StringTask type
        the function inserts the task into the queue
        """
        task = Node(task)
        inserted = 0
        self.__current = self.__head
        if (self.__current == None):
            # in case the queue is empty
            self.__head = task
            self.__q_length +=1
            inserted = 1
        else:
            inserted_task = task.get_priority()
            current_task = self.__current.get_priority()
        if (self.__current == self.__head) and (inserted_task > current_task):
            # in case the queue has only one node
            task.set_next(self.__head)
            self.__head = task
            self.__q_length +=1
            inserted = 1
        while (not inserted):
            if(not self.__current.has_next()) and \
                    (inserted_task <= current_task):
                # in case the priority of the inserted task is the smallest
                # then it means it should be at the end
                self.__current.set_next(task)
                inserted = 1
                self.__q_length +=1
            current_task = self.__current.get_next().get_priority()
            if (inserted_task > current_task):
                task.set_next(self.__current.get_next())
                self.__current.set_next(task)
                self.__q_length +=1
                inserted = 1
            self.__current = self.__current.get_next()
            # in case the function haven't inserted the task,
            # it advances to the next node

    def peek(self):
        """
        function that returns the task at the head of the queue
        """
        if (self.__head != None):
            # only if the head has a task it will be returned
            return self.__head.get_task()

    def deque(self):
        """
        function that returns the task at the head of the queue and removes it
        from the queue
        """
        self.__current = self.__head
        if (self.__current == None):
            return None
        self.__head = self.__head.get_next()
        self.__q_length -=1
        return self.__current.get_task()

    def get_head(self):
        """
        function that returns the head of the queue, meaning a Node type
        is returned
        """
        return self.__head

    def change_priority(self, old, new):
        """
        function that replaces the priority of a task, with a new one
        only if a task with the old priority was found in the queue
        """
        self.__current = self.__head
        found = 0
        priority = self.__current.get_priority()
        if(priority == old):
            # in case the task in the head is the one that its priority
            # needs to changed
            self.__head.get_task().set_priority(new)
            task_to_insert = self.deque()
            self.enque(task_to_insert)
            # the new priority may be lower than the old one
            found = 1
        while(not found):
            if (not self.__current.has_next()):
                # in case the priority isn't in the queue
                break
            priority = self.__current.get_next().get_priority()
            if(priority == old):
                self.__current.get_next().get_task().set_priority(new)
                if(self.__current.get_next().has_next()):
                    if(self.__current.get_next().get_next().get_task()
                                                .get_priority() != new):
                        # in case the new priority is not as the same as
                        # the priority of the next link there is no need
                        # to re enque the task
                        task_to_insert = self.__current.get_next().get_task()
                        self.__current.set_next(self.__current.get_next()
                                                            .get_next())
                        self.enque(task_to_insert)
                else:
                    # in case the task is the last in the queue
                    task_to_insert = self.__current.get_next().get_task()
                    self.__current.set_next(None)
                    self.enque(task_to_insert)
                found = 1
            else:
                # if the priority wasn't found the function
                # continues to the next task
                self.__current = self.__current.get_next()

    def __len__(self):
        """
        function that returns the length of the queue
        """
        return self.__q_length

    def __iter__(self):
        # the iterator is from PriorityQueueIterator type
        return PriorityQueueIterator(self)

    def __next__(self):
        """
        not used because the iter is from PriorityQueueIterator type
        """
        if(self.__current == None):
            raise StopIteration
        a = self.__current.get_task()
        self.__current = self.__current.get_next()
        return a

    def __str__(self):
        """
        converts all the tasks in the queue into a string
        """
        string = []
        for task in self:
            string.append(repr(task))
        string = str(string)
        string = string.replace('"','')
        return str(string)

    def __add__(self, other):
        """
        function that receives two queues from PriorityQueue type
        and combines them into one sorted queue and returns it
        """
        new_que = PriorityQueue()
        for task in self:
            new_que.enque(task)
        for task in other:
            new_que.enque(task)
        return new_que

    def __eq__(self, other):
        """
        function that returns True if the two queues that were given to it are
        equal
        """
        length = len(self)
        i = 0
        self.__current = self.__head
        other.__current = other.__head
        if (self.__q_length != other.__q_length):
            # if the length of both of the queues ain't equal
            # then they aren't equal
            return False
        else:
            while(self.__current != None):
                if(self.__current.get_task() != other.__current.get_task()):
                    return False
                else:
                    self.__current = self.__current.get_next()
                    other.__current = other.__current.get_next()

            return True





