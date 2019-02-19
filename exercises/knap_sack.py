class Item:
    def __init__(self, name, value, weight):
        self.name = name
        self.value = value
        self.weight = weight

    def __str__(self):
        return "Value: %s %d - Weight: %d" % (self.name, self.value, self.weight)

    def __repr__(self):
        return self.__str__()


items = [Item("compas", 4, 12),
         Item("cartabon", 2, 2),
         Item("regla", 2, 1),
         Item("escuadra", 1, 1),
         Item("transportardor", 10, 4),
         ]
c = 0


def ks(index, weight):
    global items
    global c
    c += 1

    if index >= len(items):
        return 0

    item = items[index]

    if item.weight > weight:
        return ks(index + 1, weight)
    else:

        a = max(ks(index + 1, weight),
                ks(index + 1, weight - item.weight) + item.value)
        return a


print("Max sum: %d" % (ks(0, 20),))
print("Iterations %d" % (c,))
