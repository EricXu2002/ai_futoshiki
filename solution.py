class Futoshiki:
    def __init__(self, numbers, col_ieq, row_ieq):
        self.numbers = numbers
        self.col_ieq = self.process_ieq(col_ieq, 0)
        self.row_ieq = self.process_ieq(row_ieq, 1)
        self.cell_values = self.enumerate_cells(numbers)
    
    def process_ieq(self, inequalities, direction):
        restrictions = {}
        if direction == 0: # columnwise restrictions
            for row in range(5):
                for column in range(4):
                    if inequalities[row][column] != "0":
                        restrictions[(row, column, column + 1)] = inequalities[row][column]
                        # this holds the location of the inequality and the inequality symbol
        else: # rowwise restrictions
            for row in range(4):
                for column in range(5):
                    if inequalities[row][column] != "0":
                        restrictions[(row, column, column + 1)] = inequalities[row][column]
                        # this holds the location of the inequality and the inequality symbol
        return restrictions
    
    def enumerate_cells(self, numbers):
        # an inefficient but complete method to figure out the possible values for each cell.
        rows = {"0":["1","2","3","4","5"],
                "1":["1","2","3","4","5"],
                "2":["1","2","3","4","5"],
                "3":["1","2","3","4","5"],
                "4":["1","2","3","4","5"]}
        columns = {"0":["1","2","3","4","5"],
                "1":["1","2","3","4","5"],
                "2":["1","2","3","4","5"],
                "3":["1","2","3","4","5"],
                "4":["1","2","3","4","5"]}

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
                    for num in ('1','2','3','4','5'):
                        if num in rows[str(row)] and num in columns[str(column)]:
                            possible.append(num)
                    
                    cell_values[(row, column)] = possible
        
        return cell_values