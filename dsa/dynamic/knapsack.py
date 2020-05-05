def knapsack_naive(items, capacity, item=0):
    if item == len(items) or capacity == 0:
        return 0
    value, weight = items[item]
    return max(
        knapsack_naive(items, capacity, item + 1),
        0 if capacity < weight else value + knapsack_naive(items, capacity - weight, item + 1)
    )


def knapsack_dynamic(items, capacity):
    k = [[0 for x in range(capacity + 1)] for x in range(len(items) + 1)]
    for i in range(1, len(items) + 1):
        value, weight = items[i - 1] if i > 0 else (0, 0)
        for c in range(1, capacity + 1):
            k[i][c] = 0 if i == 0 or c == 0 else max(k[i - 1][c], 0 if c < weight else value + k[i - 1][c - weight])
    return k[-1][-1]


def knapsack_memo(items, capacity, item=0, memo={}):
    if item == len(items) or capacity == 0:
        return 0
    if memo.setdefault(item, {}).setdefault(capacity, 0) == 0:
        value, weight = items[item]
        memo[item][capacity] = max(
            knapsack_memo(items, capacity, item + 1, memo),
            0 if capacity < weight else value + knapsack_memo(items, capacity - weight, item + 1, memo)
        )
    return memo[item][capacity]


def test():
    from ..util import match
    items = [(60, 10), (100, 20), (120, 30)]
    capacity = 50
    match([
        (knapsack_naive, [items, capacity], 220),
        (knapsack_dynamic, [items, capacity], 220),
        (knapsack_memo, [items, capacity], 220)
    ])


if __name__ == '__main__':
    test()
