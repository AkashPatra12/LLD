'''
    Build a custom hash map - such that
    insert, get and remove are the order of O(1)
'''


class Entry:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.active = True


class CustomHashMap:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.size = 0
        self.buckets = [None] * self.capacity

    def _hash(self, key):
        return key % self.capacity

    def get(self, key):
        index = self._hash(key)
        o_index = index

        while self.buckets[index]:
            if self.buckets[index].key == key:
                return self.buckets[index].value
            index = (index + 1) % self.capacity
            if index == o_index:
                break
        return None

    def remove(self, key):
        index = self._hash(key)
        o_index = index

        while self.buckets[index]:
            if self.buckets[index].key == key and self.buckets[index].active:
                self.buckets[index].active = False
                self.size -= 1
                return
            index = (index + 1) % self.capacity
            if index == o_index:
                break

    def insert(self, key, value):
        index = self._hash(key)
        o_index = index
        if self.buckets[index] is None:
            self.buckets[index] = Entry(key, value)
            self.size += 1
            print(index, self.buckets)
            return

        while self.buckets[index]:
            index = (index + 1) % self.capacity
            print(index)
            if index == o_index:
                raise Exception("resize required")
            if self.buckets[index] is None:
                self.buckets[index] = Entry(key, value)
                self.size += 1
                return


# 1, 11, 21, 31, 41: capcity - 5
# get (1) get(11) get(21) get(1) get(11)


customMap = CustomHashMap(5)
customMap.insert(1, 1)
customMap.insert(11, 11)
customMap.insert(21, 21)
customMap.insert(31, 31)
customMap.insert(41, 41)

print(customMap.buckets)

print(customMap.get(1))

print(customMap.get(11))

print(customMap.get(21))

print(customMap.get(31))

print(customMap.get(41))