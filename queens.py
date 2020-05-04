def change(row, col, table, place=True):
    inc = 1 if place else -1
    for i in range(len(table)):
        table[i][col] += inc
        table[row][i] += inc
        dl_col = col - row + i
        dr_col = col + row - i
        if 0 <= dl_col < len(table):
            table[i][dl_col] += inc
        if 0 <= dr_col < len(table):
            table[i][dr_col] += inc


def queens(table, placed=0):
    if placed == len(table):
        return []
    row = placed
    for col in range(len(table)):
        if table[row][col] != 0:
            continue
        change(row, col, table, True)
        result = queens(table, placed + 1)
        if result != False:
            result.append((row, col))
            return result
        change(row, col, table, False)
    return False


def test():
    ns = [8, 12, 16, 20]
    for n in ns:
        print('N =', n, queens([[0] * n for i in range(n)]))


if __name__ == '__main__':
    test()
