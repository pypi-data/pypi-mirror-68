class Heap:
    def __init__(self, comparator=lambda x, y: x > y):
        self.comparator = comparator
        self.pq = [0]
        self.qp = {}

    def heapify(self, keys):
        self.pq = [0] + keys
        self.qp = dict(zip(keys, range(1, len(self.pq))))
        k = (len(self.pq) - 1) // 2
        while k >= 1:
            self._sink(k)
            k -= 1

    def push(self, key):
        self.pq.append(key)
        self.qp[key] = len(self)
        self._swim(len(self))

    def pop(self):
        if len(self) == 0:
            raise Exception('Priority queue underflow')
        m = self.pq[1]
        self._exch(1, len(self))
        self.pq.pop()
        self._sink(1)
        del self.qp[m]
        return m

    def peek(self):
        if len(self) == 0:
            raise Exception('Priority queue underflow')
        return self.pq[1]

    def __len__(self):
        return len(self.pq) - 1

    def __delitem__(self, key):
        self._validate(key)
        i = self.qp[key]
        if i == len(self):
            self.pq.pop()
            del self.qp[key]
            return
        self._exch(i, len(self))
        self.pq.pop()
        self._swim(i)
        self._sink(i)
        del self.qp[key]

    def _validate(self, key):
        if key not in self:
            raise ValueError("index is not in the priority queue")

    def __contains__(self, item):
        return item in self.qp

    def __compare(self, i, j):
        return self.comparator(self.pq[i], self.pq[j])

    def _exch(self, i, j):
        swap = self.pq[i]
        self.pq[i] = self.pq[j]
        self.pq[j] = swap
        self.qp[self.pq[i]] = i
        self.qp[self.pq[j]] = j

    def _swim(self, k):
        while k > 1 and self.__compare(k // 2, k):
            self._exch(k, k // 2)
            k = k // 2

    def _sink(self, k):
        while 2 * k <= len(self):
            j = 2 * k
            if j < len(self) and self.__compare(j, j + 1):
                j += 1
            if not self.__compare(k, j):
                break
            self._exch(k, j)
            k = j


# order (index,value) pairs by value
class IndexHeap(Heap):
    def __init__(self, comparator=lambda x, y: x > y):
        self.map = {}
        super().__init__(lambda i, j: comparator(self.map[i], self.map[j]))

    def heapify(self, di: dict):
        self.map = dict(di)
        super().heapify(list(di.keys()))

    def pop(self):
        m = super().pop()
        value = self.map[m]
        del self.map[m]
        return m, value

    def peek(self):
        m = super().peek()
        return m, self.map[m]

    def push(self, index, value=None):
        if index in self:
            raise ValueError("index is already in the priority queue")
        if value is None:
            raise ValueError("lack value parameter")
        self.map[index] = value
        super().push(index)

    def __contains__(self, item):
        return item in self.map

    def __setitem__(self, key, value):
        self._validate(key)
        self.map[key] = value
        self._swim(self.qp[key])
        self._sink(self.qp[key])

    def __getitem__(self, item):
        self._validate(item)
        return self.map[item]

    def __delitem__(self, key):
        del super()[key]
        del self.map[key]


if __name__ == "__main__":
    a = list(range(10))
    h = Heap()
    h.heapify(a)
    h.push(5)
    h.pop()
    h.peek()
    res = []
    while len(h) > 0:
        res.append(h.pop())

    a = list(range(10))
    di = dict(zip(a, a[::-1]))
    h = IndexHeap()
    h.heapify(di)
    h[0] = 5.5
    h.push(10, 2)
    h.pop()
    h.peek()
    res = []
    while len(h) > 0:
        res.append(h.pop()[1])
