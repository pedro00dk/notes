def queens(n, / , *, placed=0, table=None):
    if placed == 0:
        table = [[0] * n for i in range(n)]
    if placed == n:
        return []
    row = placed
    for col in range(len(table)):
        if table[row][col] != 0:
            continue
        place(row, col, inc=1, table=table)
        if (result:= queens(n, table=table, placed=placed + 1)) is not None:
            result.append((row, col))
            return result
        place(row, col, inc=-1, table=table)
    return None


def place(row, col, / , *, inc=0, table=None):
    for i in range(len(table)):
        table[i][col] += inc
        table[row][i] += inc
        if 0 <= (dl_col:= col - row + i) < len(table):
            table[i][dl_col] += inc
        if 0 <= (dr_col:= col + row - i) < len(table):
            table[i][dr_col] += inc


def test():
    ns = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20]
    for n in ns:
        print('N =', n, queens(n))


if __name__ == '__main__':
    test()
