import typing
import copy
import math

class Vector:
    """
    A class representing a one-dimensional vector with various operations and access methods.
    
    Supports:
    - Initialization from list or with specific dimensions
    - Basic vector operations
    - Type checking and validation
    - Deep copying
    - Flexible indexing
    """
    
    def __init__(self, 
                 data: typing.Optional[typing.List[float]] = None, 
                 size: int = 0, 
                 fill_value: float = 0.0):
        """
        Initialize a vector.
        
        Args:
            data (list, optional): Initial vector data
            size (int, optional): Number of elements if creating an empty vector
            fill_value (float, optional): Value to fill empty vector with
        
        Raises:
            ValueError: If input data is invalid
        """
        if data is not None:
            # Deep copy the input data to prevent external modifications
            self._data = list(data)
        else:
            # Create vector with specified size and fill value
            self._data = [fill_value] * size
    
    def __getitem__(self, key):
        """
        Supports indexing and slicing
        """
        if isinstance(key, slice):
            # Return a new Vector with sliced elements
            return Vector(self._data[key])
        
        return self._data[key]
    
    def __setitem__(self, key, value):
        """
        Allows setting specific elements
        """
        self._data[key] = value
    
    def __repr__(self):
        """String representation of the vector"""
        return ' '.join(map(str, self._data))
    
    def __str__(self):
        """Formatted string representation"""
        return self.__repr__()
    
    def copy(self):
        """
        Create a deep copy of the vector
        
        Returns:
            Vector: A new independent vector
        """
        return Vector(copy.deepcopy(self._data))
    
    @property
    def size(self):
        """
        Returns the number of elements in the vector
        
        Returns:
            int: Vector length
        """
        return len(self._data)
    
    def get(self, index: int) -> float:
        """
        Safely retrieve a vector element
        
        Args:
            index (int): Element index
        
        Returns:
            float: Vector element
        
        Raises:
            IndexError: If index is out of bounds
        """
        if 0 <= index < len(self._data):
            return self._data[index]
        raise IndexError("Vector index out of range")
    
    def set(self, index: int, value: float):
        """
        Safely set a vector element
        
        Args:
            index (int): Element index
            value (float): Value to set
        
        Raises:
            IndexError: If index is out of bounds
        """
        if 0 <= index < len(self._data):
            self._data[index] = value
        else:
            raise IndexError("Vector index out of range")
    
    def dot(self, other: 'Vector') -> float:
        """
        Compute dot product with another vector
        
        Args:
            other (Vector): Vector to compute dot product with
        
        Returns:
            float: Dot product result
        
        Raises:
            ValueError: If vectors have different lengths
        """
        if self.size != other.size:
            raise ValueError("Vectors must have the same length")
        
        return sum(a * b for a, b in zip(self._data, other._data))
    
    def magnitude(self) -> float:
        """
        Compute vector magnitude (length)
        
        Returns:
            float: Vector magnitude
        """
        return math.sqrt(sum(x * x for x in self._data))


