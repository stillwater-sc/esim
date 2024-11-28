import copy
import typing

class Matrix:
    """
    A class representing a two-dimensional matrix with various operations and access methods.
    
    Supports:
    - Initialization from list of lists or with specific dimensions
    - Basic matrix operations
    - Type checking and validation
    - Deep copying
    - Flexible indexing
    """
    
    def __init__(self, 
                 data: typing.Optional[typing.List[typing.List[float]]] = None, 
                 rows: int = 0, 
                 cols: int = 0, 
                 fill_value: float = 0.0):
        """
        Initialize a matrix.
        
        Args:
            data (list of lists, optional): Initial matrix data
            rows (int, optional): Number of rows if creating an empty matrix
            cols (int, optional): Number of columns if creating an empty matrix
            fill_value (float, optional): Value to fill empty matrix with
        
        Raises:
            ValueError: If input data is inconsistent
        """
        if data is not None:
            # Validate input data
            if not data:
                self._data = []
                return
            
            # Check that all rows have the same length
            row_lengths = set(len(row) for row in data)
            if len(row_lengths) > 1:
                raise ValueError("All rows must have the same length")
            
            # Deep copy the input data to prevent external modifications
            self._data = [list(row) for row in data]
        else:
            # Create matrix with specified dimensions and fill value
            self._data = [[fill_value for _ in range(cols)] for _ in range(rows)]
    
    def __getitem__(self, key):
        """
        Supports multiple indexing methods:
        - Single index: matrix[i] returns entire row
        - Double index: matrix[i][j] returns specific element
        - Slice: matrix[1:3] returns submatrix
        """
        if isinstance(key, slice):
            # Return a new Matrix with sliced rows
            return Matrix(self._data[key])
        
        return self._data[key]
    
    def __setitem__(self, key, value):
        """
        Allows setting entire rows or specific elements
        """
        if isinstance(value, list):
            # Set entire row
            if len(value) != len(self._data[0]):
                raise ValueError("Row length must match matrix width")
            self._data[key] = list(value)
        else:
            # Set specific element
            self._data[key] = value
    
    def __repr__(self):
        """String representation of the matrix"""
        return '\n'.join([' '.join(map(str, row)) for row in self._data])
    
    def __str__(self):
        """Formatted string representation"""
        return self.__repr__()
    
    def copy(self):
        """
        Create a deep copy of the matrix
        
        Returns:
            Matrix: A new independent matrix
        """
        return Matrix(copy.deepcopy(self._data))
    
    @property
    def shape(self):
        """
        Returns the dimensions of the matrix
        
        Returns:
            tuple: (rows, columns)
        """
        if not self._data:
            return (0, 0)
        return (len(self._data), len(self._data[0]))
    
    def get(self, row: int, col: int) -> float:
        """
        Safely retrieve a matrix element
        
        Args:
            row (int): Row index
            col (int): Column index
        
        Returns:
            float: Matrix element
        
        Raises:
            IndexError: If indices are out of bounds
        """
        if 0 <= row < len(self._data) and 0 <= col < len(self._data[0]):
            return self._data[row][col]
        raise IndexError("Matrix indices out of range")
    
    def set(self, row: int, col: int, value: float):
        """
        Safely set a matrix element
        
        Args:
            row (int): Row index
            col (int): Column index
            value (float): Value to set
        
        Raises:
            IndexError: If indices are out of bounds
        """
        if 0 <= row < len(self._data) and 0 <= col < len(self._data[0]):
            self._data[row][col] = value
        else:
            raise IndexError("Matrix indices out of range")
    
    def transpose(self):
        """
        Returns the transpose of the matrix
        
        Returns:
            Matrix: Transposed matrix
        """
        if not self._data:
            return Matrix()
        
        # Create transposed matrix
        transposed = list(map(list, zip(*self._data)))
        return Matrix(transposed)
    
    def __add__(self, other):
        """
        Matrix addition
        
        Args:
            other (Matrix): Matrix to add
        
        Returns:
            Matrix: Result of addition
        
        Raises:
            ValueError: If matrices have different dimensions
        """
        if self.shape != other.shape:
            raise ValueError("Matrices must have the same dimensions")
        
        result = []
        for i in range(self.shape[0]):
            row = [self._data[i][j] + other._data[i][j] for j in range(self.shape[1])]
            result.append(row)
        
        return Matrix(result)
