from collections import defaultdict
from collections import OrderedDict

class Node:
    def __init__(self, key, count):
        self.key = key
        self.count = count


class LFU(object):
    def __init__(self, capacity):
        self.cap = capacity
        self.key2node = {}
        self.count2node = defaultdict(OrderedDict)
        self.minCount = None

    def get(self, key):
        if key not in self.key2node:
            return -1

        node = self.key2node[key]
        del self.count2node[node.count][key]

        if not self.count2node[node.count]:
            del self.count2node[node.count]

        node.count += 1
        self.count2node[node.count][key] = node

        if not self.count2node[self.minCount]:
            self.minCount += 1

        return node.key

    def put(self, key):
        if not self.cap:
            return

        if key in self.key2node:
            self.key2node[key].val = key
            self.get(key)  # NOTICE, put makes count+1 too
            return

        if len(self.key2node) == self.cap:
            k, n = self.count2node[self.minCount].popitem(last=False)
            del self.key2node[k]

        self.count2node[1][key] = self.key2node[key] = Node(key, 1)
        self.minCount = 1
        return


class LRU(OrderedDict):
    def __init__(self, capacity):
        self.capacity = capacity

    def get(self, key):
        if key not in self:
            return -1
        self.move_to_end(key)
        return self[key]

    def put(self, key):
        if key in self:
            self.move_to_end(key)
        self[key] = key
        if len(self) > self.capacity:
            self.popitem(last=False)


class MRU(OrderedDict):
    def __init__(self, capacity):
        self.capacity = capacity

    def get(self, key):
        if key not in self:
            return -1
        self.move_to_end(key)
        return self[key]

    def put(self, key):
        if key in self:
            self.move_to_end(key)
        if len(self) >= self.capacity:
            self.popitem()
        self[key] = key


class FIFO(OrderedDict):
    def __init__(self, capacity):
        self.capacity = capacity

    def get(self, key):
        if key not in self:
            return -1
        return self[key]

    def put(self, key):
        if key in self:
            return
        if len(self) >= self.capacity:
            self.popitem(last=False)
        self[key] = key


def eviction_policy(cache_size, func, access):
    policy = func(cache_size)
    hit = miss = 0
    access = access.split(",")
    for i in access:
        if policy.get(i) == -1:
            miss += 1
            policy.put(i)
        else:
            hit += 1
    print(func)
    print("HIT: ", hit)
    print("MISS: ", miss)


s = "C,D,B,A,E,C,C,E,E,C,G,A,C,A,B,D,E,D,A,B"
eviction_policy(4, LRU, s)
eviction_policy(4, MRU, s)
eviction_policy(4, FIFO, s)
eviction_policy(4, LFU, s)
