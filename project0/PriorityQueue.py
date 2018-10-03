import heapq

class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.count = 0

    def isEmpty(self):
        return self.heap == []

    def push(self, item, priority):
        heapq.heappush(self.heap,(priority,item))
        self.count += 1

    def pop(self):
        self.count -= 1
        return heapq.heappop(self.heap)

    def update(self,item,priority):
        for i in self.heap:
            if(item == i[1]):
                if(i[0] > priority):
                    # update existing item priority
                    self.heap[self.heap.index(i)] = (priority,item)
                return
        else:
            self.push(item,priority)

def PQSort(intlist):
    pq = PriorityQueue()
    result = []
    for i in intlist:
        pq.push(i,i)
    while (not pq.isEmpty()):
        result.append(pq.pop()[1])
    return result


if __name__ == '__main__':

    pq = PriorityQueue()
    intlist = [1,3,2]
    print PQSort(intlist)
    # pq.push("task1", 1)
    # pq.push("task2", 3)
    # pq.push("task3", 2)
    # print pq.heap,pq.count
    # pq.update("task2", 2)
    # pq.update("task1", 2)
    # print pq.heap,pq.count
    # print pq.pop(),pq.count
    # print pq.pop(),pq.count
    # print pq.pop(),pq.count