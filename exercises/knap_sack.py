class Item:
    def __init__(self, name, value, weight):
        self.name = name
        self.value = value
        self.weight = weight

    def __str__(self):
        return "Value: %s %d - Weight: %d" % (self.name, self.value, self.weight)

    def __repr__(self):
        return self.__str__()


def knapsack_resolver(index, weight, items):
    c = 0
    c += 1

    if index >= len(items):
        return 0

    item = items[index]

    if item.weight > weight:
        return knapsack_resolver(index + 1, weight, items)
    else:
        a = max(knapsack_resolver(index + 1, weight, items),
                knapsack_resolver(index + 1, weight - item.weight, items) + item.value)
        return a
