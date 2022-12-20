def process_ieq(inequalities, direction):
    restrictions = {}
    if direction == 0:  # column-wise restrictions
        for row in range(5):
            for column in range(4):
                if inequalities[row][column] != "0":
                    # restrictions[(row, column, column + 1)] = inequalities[row][column]

                    if inequalities[row][column] == '<':
                        restrictions[(row, column)] = 'l'+inequalities[row][column]+'r'
                        restrictions[(row, column+1)] = 'r'+'>'+'l'
                    else:
                        restrictions[(row, column)] = 'l'+inequalities[row][column]+'r'
                        restrictions[(row, column+1)] = 'r'+'<'+'l'
                    # this holds the location of the inequality and the inequality symbol
    else:  # row-wise restrictions
        for row in range(4):
            for column in range(5):
                if inequalities[row][column] != "0":
                    # restrictions[(row+1, column)] = inequalities[row][column]
                    if inequalities[row][column] == '^':
                        restrictions[(row+1, column)] = 'd>u'
                        restrictions[(row, column)] = 'u<d'
                    else:
                        restrictions[(row+1, column)] = 'd<u'
                        restrictions[(row, column)] = 'u>d'
                    # this holds the location of the inequality and the inequality symbol
    return restrictions


def enumerate_cells(numbers):
    # an inefficient but complete method to figure out the possible values for each cell.
    rows = {"0": ["1", "2", "3", "4", "5"],
            "1": ["1", "2", "3", "4", "5"],
            "2": ["1", "2", "3", "4", "5"],
            "3": ["1", "2", "3", "4", "5"],
            "4": ["1", "2", "3", "4", "5"]}
    columns = {"0": ["1", "2", "3", "4", "5"],
               "1": ["1", "2", "3", "4", "5"],
               "2": ["1", "2", "3", "4", "5"],
               "3": ["1", "2", "3", "4", "5"],
               "4": ["1", "2", "3", "4", "5"]}

    cell_values = {}

    # first, go through the entire set and find the pre-determined values.
    for row in range(5):
        for column in range(5):
            curr_value = numbers[row][column]
            if curr_value != "0":
                rows[str(row)].remove(curr_value)
                columns[str(column)].remove(curr_value)
                cell_values[(row, column)] = curr_value

    # then, go through the set and fully populate the cell_values dictionary
    for row in range(5):
        for column in range(5):
            # perform a sort of "inner join" on the corresponding row/column to figure out the possible values for a cell
            if (row, column) not in cell_values:
                possible = []
                for num in ('1', '2', '3', '4', '5'):
                    if num in rows[str(row)] and num in columns[str(column)]:
                        possible.append(num)
                cell_values[(row, column)] = possible
    return cell_values


class Futoshiki:
    def __init__(self, numbers, col_ieq, row_ieq):
        self.numbers = numbers
        self.col_ieq = process_ieq(col_ieq, 0)
        self.row_ieq = process_ieq(row_ieq, 1)
        self.cell_values = enumerate_cells(numbers)
        self.csp = self.find_csp()
        self.vars = 25
        self.domain = ['1', '2', '3', '4', '5']

    def find_csp(self):
        csp = {}
        for k, v in self.cell_values.items():
            if isinstance(v, str):
                continue
            else:
                csp[k] = v
        return csp

    def mrv_h(self):
        min_csp = 10
        csp = []
        for v in self.csp.values():
            min_csp = min(min_csp, len(v))
        for k, v in self.csp.items():
            if len(v) == min_csp:
                csp.append(k)
        return csp

    def degree_h(self, csp):
        dire = [-1, 0, 1, 0, -1]
        max_neighbor = -1
        var = 0
        for k in csp:
            neighbor = 0
            for i in range(len(dire)-1):
                row = dire[i]
                col = dire[i+1]
                if 0 <= row <= 4 and 0 <= col <= 4 and self.numbers[row][col] == "0":
                    neighbor += 1
            if max_neighbor < neighbor:
                max_neighbor = neighbor
                var = k
        return var

    def check_consistent(self, var, val):
        row, col = var[0], var[1]
        if (row, col) in self.col_ieq:
            if self.col_ieq[(row, col)] == 'l>r':
                if self.numbers[row][col+1] != '0' and int(val) < int(self.numbers[row][col+1]):
                    return False
            elif self.col_ieq[(row, col)] == 'r<l':
                if self.numbers[row][col-1] != '0' and int(val) > int(self.numbers[row][col-1]):
                    return False
            elif self.col_ieq[(row, col)] == 'l<r':
                if self.numbers[row][col+1] != '0' and int(val) > int(self.numbers[row][col+1]):
                    return False
            else:  # r>l
                if self.numbers[row][col-1] != '0' and int(val) < int(self.numbers[row][col-1]):
                    return False
        if (row, col) in self.row_ieq:
            if self.row_ieq[(row, col)] == 'd>u':
                if self.numbers[row-1][col] != '0' and int(val) < int(self.numbers[row-1][col]):
                    return False
            elif self.row_ieq[(row, col)] == 'u<d':
                if self.numbers[row+1][col] != '0' and int(val) > int(self.numbers[row+1][col]):
                    return False
            elif self.row_ieq[(row, col)] == 'd<u':
                if self.numbers[row-1][col] != '0' and int(val) > int(self.numbers[row-1][col]):
                    return False
            else:  # u>d
                if self.numbers[row+1][col] != '0' and int(val) < int(self.numbers[row+1][col]):
                    return False
        for i in range(5):
            if self.numbers[i][col] == val:
                return False
            if self.numbers[row][i] == val:
                return False
        return True

    def del_csp(self, var):
        del self.csp[var]
        return

    def add_csp(self, var, var_value):
        self.csp[var] = var_value
        return

    def add_numbers(self, var, val):
        row, col = var[0], var[1]
        self.numbers[row][col] = val
        return

    def del_numbers(self, var):
        row, col = var[0], var[1]
        self.numbers[row][col] = '0'
        return

    def backtrack(self):
        if len(self.csp) == 0:
            return self.numbers
        var = self.mrv_h()
        if len(var) > 1:
            var = self.degree_h(var)
        else:
            var = var[0]
        for val in self.domain:
            if self.check_consistent(var, val):
                self.vars -= 1
                var_value = self.csp[var]
                self.del_csp(var)
                self.add_numbers(var, val)
                result = self.backtrack()
                if result:
                    return result
                else:
                    self.add_csp(var, var_value)
                    self.del_numbers(var)
        self.vars += 1
        return False


def main():
    with open("Input3.txt") as sample:
        parsed = sample.read()
        items = parsed.split("\n")
        numbers = [row.split() for row in items[:5]]
        col_ieq = [row.split() for row in items[6:11]]
        row_ieq = [row.split() for row in items[12:17]]
        print(f'{numbers=}')
        print(f'{row_ieq=}')
        print(f'{col_ieq=}')

    futoshiki1 = Futoshiki(numbers, col_ieq, row_ieq)
    print(f'{futoshiki1.cell_values=}')
    print(f'{futoshiki1.col_ieq=}')
    print(f'{futoshiki1.row_ieq=}')
    # print(f'{futoshiki1.csp=}')
    # mrv = futoshiki1.mrv_h()
    # print(f'{mrv=}')
    # if len(mrv) > 1:
    #     print(f'{futoshiki1.degree_h(mrv)=}')
    solution = futoshiki1.backtrack()
    print(f'{solution=}')

    with open("Output3.txt", "w") as out:
            output = ""
            output += ("\n".join([" ".join(row) for row in solution]) + "\n\n")

            out.write(output)


if __name__ == '__main__':
    main()
