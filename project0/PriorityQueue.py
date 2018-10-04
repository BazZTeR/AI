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
        # item doesnt exist in PQ so we push it
        self.push(item,priority)

def PQSort(intlist):
    pq = PriorityQueue()
    result = []
    # heap requires (priority,item) and because we only want to sort integers we push the same value to both priority and item
    for i in intlist:
        pq.push(i,i)
    while (not pq.isEmpty()):
        result.append(pq.pop()[1])
    return result

# A simple main to test the code
if __name__ == '__main__':
    pq = PriorityQueue()
    pq.push("task1", 1)
    pq.push("task2", 2)
    pq.push("task3", 0)
    print "Added 3 new tasks:",pq.heap,",count =",pq.count
    print "Updating tasks..."
    pq.update("task2", 3)
    pq.update("task1", 0)
    pq.update("task4", 5)
    pq.update("task4", 6)
    print "Tasks after update: ",pq.heap,",count =",pq.count
    print "Popping tasks with ascending priority order:"
    while (not pq.isEmpty()):
        print pq.pop(),",count =",pq.count
    print "----------------------------------------------"
    intlist = [1,3,2,5,4,9,8,6]
    print "Orderind list:",intlist,"using PQSort"
    print "Sorted:",PQSort(intlist)