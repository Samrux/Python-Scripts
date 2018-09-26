from math import isclose
from itertools import chain
from numbers import Number


class Matrix:
    def __init__(self, rows: iter):
        """Creates a new matrix from an iterable of iterables"""
        if len(rows) == 0 or len(rows[0]) == 0:
            self._list = []
        else:
            self._list = Matrix.zero(len(rows), len(rows[0]))._list
            self.fill(lambda r, c: rows[r][c])

    @classmethod
    def raw(cls, rows: list):
        """Creates a new matrix and sets its internal list of elements to the provided list. Use with caution"""
        matrix = cls.__new__(cls)  # Empty Matrix object
        matrix._list = rows
        return matrix

    @classmethod
    def zero(cls, m, n):
        """Creates a new matrix with m rows and n columns, filled with zeros"""
        return Matrix.raw([[0]*n for _ in range(m)])

    @classmethod
    def identity(cls, n):
        """Creates an identity matrix of size n, which is the neutral element of nxn matrix multiplication"""
        matrix = Matrix.zero(n, n)
        for i in range(n):
            matrix[i, i] = 1
        return matrix
        
    @classmethod
    def elementary(cls, n, **kwargs):        
        """Creates an elementary matrix of size n, which is an identity matrix affected by a row operation.
        Keyword arguments: i,j for row swapping; i,k for row multiplication; i,j,k for row addition.
        """
        return Matrix.identity(n).elem(**kwargs)


    # Operations
    
    def __matmul__(self, other: 'Matrix'):  # @
        if self.columns != other.rows:
            raise ValueError('The first matrix must have as many columns as the second has rows')
        return Matrix.zero(self.rows, other.columns)\
            .fill(lambda r, c: sum(self[r, i]*other[i, c] for i in range(other.rows)))
    
    def __iadd__(self, other: 'Matrix'):  # +=
        if self.size != other.size:
            raise ValueError('The two matrices must have equal dimensions')
        return self.fill(lambda r, c: self[r, c]+other[r, c])
                
    def __imul__(self, k: Number):  # *=
        return self.fill(lambda r, c: self[r, c]*k)

    def __ipow__(self, p: int):  # **=
        if not self.is_square and p not in (+1, -1):
            raise ValueError("Can't raise a non-square matrix")
        if p == 0:
            return Matrix.identity(self.rows)

        new = self.copy()
        if p < 0:
            new = new.inverse()
            p = -p
        while p > 1:
            new @= self
            p -= 1
        return new

    def minor(self, r, c):
        """Obtains a minor of this matrix for the given row and column"""
        return self.submatrix([r], [c]).determinant

    def submatrix(self, delr, delc):
        """Creates a submatrix that has all the specified rows and columns deleted"""
        return Matrix.raw([[self[i, j] for j in range(self.columns) if j not in delc]
                           for i in range(self.rows) if i not in delr])

    def transpose(self):
        """Creates the transpose of this matrix, which is flipped along its diagonal"""
        return Matrix.zero(self.columns, self.rows).fill(lambda r, c: self[c, r])

    def cofactor(self):
        """Creates the cofactor of this matrix, whose elements have alternating signs"""
        return Matrix.zero(*self.size).fill(lambda r, c: self[r, c] * (-1)**((r+c)%2))

    def adjugate(self):
        """Creates the adjugate of this matrix, which is the transpose of its cofactor"""
        return self.cofactor().transpose()

    def inverse(self):
        """Creates the multiplicative inverse of this matrix"""
        det = self.determinant if self.is_square else 0
        if det == 0:
            return None
        minors = Matrix.zero(*self.size).fill(lambda r, c: self.minor(r, c))
        return minors.adjugate() * (1/det)

    def rowadd(self, i: int, j: int, k: Number = 1):
        """Adds row j times k to row i"""
        for c in range(self.columns):
            self[i, c] += self[j, c] * k
        return self

    def rowmult(self, i: int, k: Number):
        """Multiplies row i by k"""
        for c in range(self.columns):
            self[i, c] *= k
        return self

    def rowswap(self, i: int, j: int):
        """Swaps rows i and j"""
        for c in range(self.columns):
            self[i, c], self[j, c] = self[j, c], self[i, c]
        return self

    def elem(self, **kwargs):
        """Applies an elementary row operation to this matrix.
        Arguments: i,j for swapping; i,k for multiplication; i,j,k for addition.
        """
        i = kwargs.get('i')
        j = kwargs.get('j', None)
        k = kwargs.get('k', None)

        if j is None:
            if k is None:
                raise NameError('Please specify j and/or k')
            return self.rowmult(i, k)
        else:
            return self.rowswap(i, j) if k is None else self.rowadd(i, j, k)


    # Properties
    
    @property
    def rows(self):
        """Number of rows in this matrix"""
        return len(self._list)
    
    @property
    def columns(self):
        """Number of columns in this matrix"""
        return len(self._list[0])
        
    @property
    def size(self):
        """Tuple with the numbers of rows and columns in this matrix"""
        return self.rows, self.columns

    @property
    def determinant(self):
        """Obtain the determinant of this matrix"""
        if not self.is_square:
            raise ValueError('A non-square matrix has no determinant')
        if self.size == (2, 2):
            return self[0, 0] * self[1, 1] - self[0, 1] * self[1, 0]
        else:
            return sum(self[0, c] * self.minor(0, c) * (-1)**(c%2) for c in range(self.columns))

    @property
    def is_square(self):
        """Whether this matrix has the same numbers of rows and columns"""
        return self.rows == self.columns

    @property
    def is_invertible(self):
        """Whether this matrix can be inverted. It is recommended to instead check whether inverse() returns None."""
        return not self.is_square or self.determinant == 0

    @property
    def is_singular(self):
        """Whether this matrix is not invertible"""
        return not self.is_invertible

    @property
    def is_identity(self):
        """Whether this matrix is an identity matrix"""
        return all(isclose(self[r, c], 1 if r == c else 0) for r, c in self.all_positions())

    @property
    def is_echelon(self):
        """Whether this matrix is in row echelon form"""
        zero_row = False
        for r in range(self.rows-1):
            for c in range(self.columns):
                if self[r, c] != 0:  # First
                    if zero_row or self[r+1, c] != 0:
                        return False
                    break
            else:  # Didn't break
                zero_row = True
        return True


    # Other methods
        
    def row(self, i):
        """Returns all elements in a given row"""
        return tuple(self[i, c] for c in range(self.columns))
    
    def column(self, j):
        """Returns all elements in a given column"""
        return tuple(self[r, j] for r in range(self.rows))

    def diagonal(self):
        """Returns the elements of this matrix along its diagonal"""
        return tuple(self[i, i] for i in range(min(self.rows, self.columns)))

    def all_positions(self):
        """Returns all (i,j) positions in this matrix"""
        return chain.from_iterable(((r, c) for r in range(self.rows)) for c in range(self.columns))
    
    def fill(self, func):
        """Fills the matrix using a function as a value"""
        for r in range(self.rows):
            for c in range(self.columns):
                self[r, c] = func(r, c)
        return self
        
    def copy(self):
        """Creates a copy of this matrix"""
        new = Matrix.zero(*self.size)
        return new.fill(lambda r, c: self[r, c])


    # Other magic methods
    
    def __getitem__(self, pos: iter):
        i, j = pos
        if isinstance(i, slice):  # Slicing gets you a submatrix
            istart = i.start; istop = i.stop
            jstart = j.start; jstop = j.stop

            # Prepare all slice values... very slowly
            if istart is None: istart = 0
            elif istart < 0: istart += self.rows
            if istop is None: istop = self.rows
            elif istop < 0: istop += self.rows

            if jstart is None: jstart = 0
            elif jstart < 0: jstart += self.columns
            if jstop is None: jstop = self.columns
            elif jstop < 0: jstop += self.columns

            rows = istop-istart
            columns = jstop-jstart
            if rows < 1 or columns < 1:
                return Matrix([])
            return Matrix.zero(rows, columns).fill(lambda r, c: self[istart+r, jstart+c])
        
        else:
            return self._list[i][j]
        
    def __setitem__(self, pos: iter, val):
        i, j = pos
        self._list[i][j] = val

    def __str__(self):
        # Get formatted elements
        form = Matrix.raw([['{:.4f}'.format(self[r, c]).rstrip('0').rstrip('.') for c in range(self.columns)]
                           for r in range(self.rows)])
        # Gather ideal length for each column
        len_col = [max(len(x) for x in form.column(j)) for j in range(form.columns)]

        rows = []
        for r in range(self.rows):
            if r == 0:
                sides = ' ┌ {} ┐'
            elif r == self.rows - 1:
                sides = ' └ {} ┘'
            else:
                sides = ' │ {} │'
            rows.append(sides.format(' '.join(form[r, c].rjust(len_col[c]) for c in range(form.columns))))
        return '\n'.join(rows)

    def __repr__(self):
        return self.__str__

    def __len__(self):
        return self.rows

    def __iter__(self):
        for r in range(self.rows):
            yield self.row(r)

    def __add__(self, other):  # + uses += as a base
        return self.copy().__iadd__(other)

    def __mul__(self, k):  # * uses *= as a base
        return self.copy().__imul__(k)

    def __pow__(self, p):  # ** uses **= as a base
        return self.copy().__ipow__(p)


if __name__ == '__main__':
    M1 = Matrix(((4, 6),
                 (3, 8)))

    M2 = Matrix(((3, 0, 2),
                 (2, 0, -2),
                 (0, 1, 1)))

    M3 = Matrix(((4, 2, 3, 1, 4),
                 (0, 2, 1, 4, 0),
                 (0, 0, 0, 3, 0)))

    print('<<< Matrix demo >>>\nThis implementation was made for study, experimentation and fun\n')
    print(f'M1\n{M1}')
    print(f' M1[0, 1]: {M1[0, 1]}')
    print(f'M1^T\n{M1.transpose()}')
    print()
    print(f'M2\n{M2}')
    print(f'M2^-1\n{M2.inverse()}')  # Notice there's more than 1 way to get the inverse
    print(f'M2 x M2^-1\n{M2 @ M2**-1}')
    print(f' is_identity: {(M2 @ M2**-1).is_identity}')
    print()
    print(f'M3\n{M3}')
    print(f' is_echelon: {M3.is_echelon}')
    print(f'Submatrix M3[1:, 2:-1]\n{M3[1:, 2:-1]}')
    print(f'Elementary(i=2, j=0, k=2) @ M3\n{M3.elem(i=2, j=0, k=2)}')

