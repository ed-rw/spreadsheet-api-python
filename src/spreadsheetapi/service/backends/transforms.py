import re


class CellsToView:
    def __init__(self, cells):
        self.cells = cells

    def view(self):
        if len(self.cells) > 0:
            array = self.cells_to_2d_array(self.cells)
            return self.array_to_string(array)
        else:
            # Hmm should this be an error instead?
            return ""

    @staticmethod
    def cells_to_2d_array(cells):
        """Transform the list of cells into a two-dimensional array.

        >>> cells = [
        ... {'name': 'A1', 'data': {'value': 'a1', 'type': 'literal'}},
        ... {'name': 'B2', 'data': {'value': 'b2', 'type': 'literal'}},
        ... {'name': 'C3', 'data': {'value': 'c3', 'type': 'literal'}}]
        >>> array = CellsToView.cells_to_2d_array(cells)
        >>> array == [['*', 'A', 'B', 'C'],
        ...           ['1', 'a1', None, None],
        ...           ['2', None, 'b2', None],
        ...           ['3', None, None, 'c3']]
        True
        """

        array = []

        for cell in cells:
            col, row = CellsToView.cell_name_parts(cell["name"])

            col_ndx = CellsToView.col_to_int(col)
            row_ndx = int(row)

            CellsToView.ensure_array_values(array, row_ndx, col_ndx)

            # Add cell value
            array[row_ndx][col_ndx] = cell["data"]["value"]
            # NOTE: When cell types allow more than literal, will need to do
            # more processing here

        # Add row and column labels
        # NOTE: Need something at 0,0 to get the browser to keep things
        # lined up correctly
        array[0][0] = "*"
        for row_ndx in range(1, len(array)):
            array[row_ndx][0] = str(row_ndx)
        for col_ndx in range(1, len(array[0])):
            array[0][col_ndx] = CellsToView.int_to_col(col_ndx)

        return array

    @staticmethod
    def ensure_array_values(array, row_ndx, col_ndx):
        """Need to fill in null data up to the desired indices, without
        changing existing data.

        >>> array_1 = []
        >>> CellsToView.ensure_array_values(array_1, 3, 3)
        >>> array_1 == [[None, None, None, None], [None, None, None, None],
        ...             [None, None, None, None], [None, None, None, None]]
        True

        >>> array_2 = [[None, None], [None, "a1", None], [None, None, "b2"]]
        >>> CellsToView.ensure_array_values(array_2, 3, 3)
        >>> array_2 == [[None, None, None, None],
        ...             [None, "a1", None, None],
        ...             [None, None, "b2", None],
        ...             [None, None, None, None]]
        True
        """

        for i in range(0, row_ndx + 1):
            if len(array) <= i:
                array.append([])

            for j in range(len(array[i]), col_ndx + 1):
                array[i].append(None)

    @staticmethod
    def cell_name_parts(cell_name):
        """Convert the given cell name to row and column indices.

        >>> CellsToView.cell_name_parts("A1")
        ('A', '1')
        >>> CellsToView.cell_name_parts("Z10")
        ('Z', '10')
        >>> CellsToView.cell_name_parts("ZZ99")
        ('ZZ', '99')
        >>> CellsToView.cell_name_parts("ABC100")
        ('ABC', '100')
        """

        match = re.match(r"([A-Z]+)([1-9][0-9]*)", cell_name)

        if match is None:
            # Corrupted data store.. *shouldn't* get here
            raise RuntimeError("Invalid cell name")

        return (match.group(1), match.group(2))

    @staticmethod
    def col_to_int(col):
        """Convert the given column name to an integer. Start counting at 1

        >>> CellsToView.col_to_int("A")
        1
        >>> CellsToView.col_to_int("Z")
        26
        >>> CellsToView.col_to_int("AA")
        27
        >>> CellsToView.col_to_int("BA")
        53
        >>> CellsToView.col_to_int("ABC")
        731
        """

        col_int = 0
        col_letters = list(col)

        for ndx, letter in enumerate(reversed(col_letters)):
            # Subtracting by 64 here makes "A" 1, not 0
            col_int += pow(26, ndx) * (ord(letter) - 64)

        return col_int

    @staticmethod
    def int_to_col(col_ndx):
        """Convert the given column index to a base 26 string.

        >>> CellsToView.int_to_col(1)
        'A'
        >>> CellsToView.int_to_col(26)
        'Z'
        >>> CellsToView.int_to_col(27)
        'AA'
        >>> CellsToView.int_to_col(53)
        'BA'
        >>> CellsToView.int_to_col(731)
        'ABC'
        """

        if col_ndx == 0:
            # O doesnt have a value is this column system
            return None

        chars = []

        while col_ndx > 0:
            col_ndx, d = divmod(col_ndx, 26)

            if d == 0:
                col_ndx, d = col_ndx - 1, d + 26

            chars.append(chr(d + 64))

        return "".join(reversed(chars))

    @staticmethod
    def array_to_string(array):
        row_strings = []
        for i in range(0, len(array)):
            row_elements = [
                element if element is not None else "" for element in array[i]
            ]
            row_strings.append("\t".join(row_elements))

        return "\n".join(row_strings)
