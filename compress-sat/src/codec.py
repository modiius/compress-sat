class TypeUInt8Exception(Exception):
    def __init__(self, value):
        self.message = f"Expected type 'UInt8', but '{type(value).__name__}' was given."
        super().__init__(self.message)

class LengthError(Exception):
    def __init__(self, value):
        self.message = f'Expected length is divisible by 8. Found length: {len(value)}.'
        super().__init__(self.message)

class UInt8:
    """ A class representaing a data type value as an unsigned int8.

    Attributes
    ----------
    - val: int|str
            the value of the number to be converted into UInt8
    
    Methods
    -----------
    - __str__ : printing the binary representation  
    - __eq__ : equality (==)
    - __add__ : addition (+)
    - __sub__ : substraction (-)
    - __lshift__ : left shift opertion (<<)
    - __rshift__ : arithmetic right shift (>>)
    - __matmul__ : logical right shift (@)
    - __xor__ : logical exclusive OR operation (^)
    - __invert__ : bit inversion (~)
    - __and__ : logical AND operation (&)
    """
    def __init__(self, val: int|str):
        """Function initializing the UInt8 class. The initialization handles the overflow (numbers higher than 255). 

        Parameters
        ----------
        - val: str or int
            a value that is to be converted into its 8 bit representation
        """
        if isinstance(val, str):
            if len(val) != 8:
                raise LengthError(val)
            self._value = int(val, 2) & 0xFF
        else:
            self._value = val & 0xFF  

    def __str__(self):
        """Method printing the binary representation of the instanciated value.
        
        Returns
        -------
        - str

        Example
        -------
        >>> str(UInt8(5))
        '00000101'
        >>> str(UInt8(17))
        '00010001'
        """
        return f"{self._value:08b}"
    
    def __eq__(self, other):
        """Method checking the equality between two UInt8 values.
        
        Parameters
        ----------
        - other: UInt8
            the other value for the comparision 
        
        Returns
        -------
        - Bool 

        Example
        -------
        >>> str(UInt8(255) == UInt8(1))
        'False'
        >>> str(UInt8(15) == UInt8(15)) 
        'True'
        Hadling overflow:
        >>> str(UInt8(257) == UInt8(1))
        'True'
        """
        if not isinstance(other, UInt8):
            raise TypeUInt8Exception(other)
        
        return self._value == other._value
    
    def __add__(self, other):
        """Method performing addition of two UInt8 values. It acts just like regular addition with overflow handling (as the result is an UInt8). 
        
        Parameters
        ----------
        - other: UInt8
            the other value that is to be added 
        
        Returns
        -------
        - UInt8

        Example
        -------
        >>> str(UInt8(5) + UInt8(17))
        '00010110'
        >>> str(UInt8(0) + UInt8(1)) 
        '00000001'
        Handling overflow:
        >>> str(UInt8(255) + UInt8(1))
        '00000000'
        """
        if not isinstance(other, UInt8):
            raise TypeUInt8Exception(other)
        
        return UInt8(self._value + other._value)

    def __sub__(self, other):
        """Method performing substractio of another UInt8 value. It acts just like regular substractio with overflow handling (as the result is an UInt8). 
        
        Parameters
        ----------
        - other: UInt8
            the other value that is to be substracted 

        Returns
        -------
        - UInt8

        Examples
        --------
        >>> str(UInt8(15) -  UInt8(15))
        '00000000'
        >>> str(UInt8(250) -  UInt8(15))
        '11101011'
        Negative numbers (wrap around):
        >>> str(UInt8(20) -  UInt8(25))    
        '11111011'
        """
        if not isinstance(other, UInt8):
            raise TypeUInt8Exception(other)
        
        return UInt8(self._value - other._value)

    def __lshift__(self, other):
        """Method performig the left shift by a given number (as UInt8).
        
        Parameters
        ----------
        - other: UInt8
            the number to shift by

        Returns
        -------
        - UInt8

        Example
        -------
        >>> str(UInt8(5))
        '00000101'
        >>> str(UInt8(5) << UInt8(2))
        '00010100'
        >>> str(UInt8(5) << UInt8(10))
        '00000000'
        """
        if not isinstance(other, UInt8):
            raise TypeUInt8Exception(other)
        
        return UInt8(self._value << other._value)
    

    def __rshift__(self, other):
        """Method performing the arithmetic right shift by a given number (as UInt8).
        
        The arithmetic right shift checks if the furthest left bit (2^7) is equal to 1 or 0 and shifts the values bits to the right, filling the gaps with the same value (either 1 or 0).
        The arithetic right shift description: https://stackoverflow.com/questions/64963170/how-to-do-arithmetic-right-shift-in-python-for-signed-and-unsigned-values

        Parameters
        ----------
        - other: UInt8
            the number to shift by

        Returns
        -------
        - UInt8

        Example
        -------
        >>> str(UInt8(200))
        '11001000'
        >>> str(UInt8(200) >> UInt8(2))
        '11110010'
        >>> str(UInt8(20))             
        '00010100'
        >>> str(UInt8(20) >> UInt8(2)) 
        '00000101'
        """
        if not isinstance(other, UInt8):
            raise TypeUInt8Exception(other)
        
        if self._value & 2**7 != 0:
            mask = int("1"*other._value + "0"*(8-other._value), 2)
            return UInt8((self._value >> other._value) | mask)
        else:
            return UInt8(self._value >> other._value)
    
    def __matmul__(self, other):
        """Method performing the logical right shift.
        
        Shifts the values bits to the right, filling the gaps always with 0.

        Parameters
        ----------
        - other: UInt8
            the number to shift by

        Returns
        -------
        - UInt8

        Example
        -------
        >>> str(UInt8(20))            
        '00010100'
        >>> str(UInt8(20) @ (UInt8(2)))
        '00000101'
        >>> str(UInt8(200))             
        '11001000'
        >>> str(UInt8(200) @ (UInt8(2)))
        '00110010'
        """
        if not isinstance(other, UInt8):
            raise TypeError(f'Expected type is UInt8 and a {type(other)} was given.')
        
        return UInt8(self._value >> other._value)
    
    def __xor__(self, other):
        """Method performig a logical exclusive OR operation on corresponding bits on two equal-lenght binary representations.. 

        If both bits are equal to 1 or 0 then the result is equal to 0, otherwise the result is equal to 1.

        Parameters
        ----------
        - other: UInt8
            the other value we are performing the logical exclusive OR operation with
        
        Returns
        -------
        - UInt8

        Example
        -------
        >>> str((UInt8(2)))             
        '00000010'
        >>> str((UInt8(6)))
        '00000110'
        >>> str((UInt8(6)^ UInt8(2)))
        '00000100'
        """
        if not isinstance(other, UInt8):
            raise TypeUInt8Exception(other)
        
        return UInt8(self._value ^ other._value)
    
    def __invert__(self):
        """Method performing bit inversion on an UInt8.

        Returns
        -------
        - UInt8        

        Example
        -------
        >>> str(UInt8(9))
        '00001001'
        >>> str(~UInt8(9))
        '11110110'
        """
        return UInt8(~self._value)
    
    def __and__(self, other):
        """Method performing a logical AND operation on two equal-lenght binary representations.

        The representations are compared bit by bit on the correspondig positions. If both bits are equal to 1 then the result is also equal to 1, otherwise the result is equal to 0. 

        Parameters
        ----------
        - other: UInt8
            the other value we are performing logical AND operation with
        
        Returns
        -------
        - UInt8
        
        Example
        -------
        >>> str(UInt8(5))             
        '00000101'
        >>> str(UInt8(1))
        '00000001'
        >>> str(UInt8(5) & (UInt8(1)))
        '00000001'
        >>> str(UInt8(5) & (UInt8(5)))
        '00000101'
        >>> str(UInt8(5) & ~(UInt8(5)))
        '00000000'

        """
        if not isinstance(other, UInt8):
            raise TypeUInt8Exception(other)
        
        return UInt8(self._value & other._value)


def as_str(data_uint8: list[UInt8]):
    
    return "".join([str(d) for d in data_uint8])


def as_uint8(data_str: str):
    if len(data_str) % 8 != 0:
        raise LengthError(data_str)
    data_uint8 = []
    for i in range(0, len(data_str), 8):
        value = UInt8(data_str[i:i+8])
        data_uint8.append(value)
    
    return data_uint8


def transpose(data: list) -> list[str]:
    if len(data) == 0:
        data_t = []
    data_t = []
    for pos in range(len(str(data[0]))): 
        row_t = ""
        for i in range(len(data)):
            row_t += str(data[i])[pos]
        data_t.append(row_t)
    
    return data_t


def encode_count(data_str: list[str]) -> tuple[int, str]:
    data_tuple = []
    for sequence in data_str:
        count = 0
        for pos in range(len(sequence)):
            if sequence[pos] == "0":
                count += 1
            else:
                break
        data_tuple.append((count, sequence[count:]))
    
    return data_tuple


def encode_zigzag(n: UInt8, k=UInt8(8)):
    return (n << UInt8(1)) ^ (n >> (k - UInt8(1)))


def compress(data: str):
    data_uint8 = as_uint8(data)
    first = data_uint8[0]
    delta = [data_uint8[i] - data_uint8[i+1] for i in range(len(data_uint8)-1)]
    zigzag = [encode_zigzag(d) for d in delta]
    zigzag_t = transpose(zigzag)
    encoded_zigzag_t = encode_count(zigzag_t)

    result = f"{len(data_uint8):016b}{str(first)}"
    for num_zeros, remainder in encoded_zigzag_t:
        result = result + f"{num_zeros:016b}" + remainder

    return result


def decode_count(data: list[tuple[int, str]]):
    data_str = []
    for num_zeros, reminder in data:
        zeros = '0' * num_zeros
        data_str.append(zeros + reminder)

    return data_str


def decode_zigzag(n: UInt8):
    return (n @ UInt8(1)) ^ (~(n & UInt8(1)) + UInt8(1))


def decompress(data: str) -> str:
    # minus one because the length is smaller by one through the delta (minusing the values from one another)
    delta_length = int(data[:16], 2) - 1
    first_value = UInt8(data[16:24])
    data = data[24:]
    encode = []
    for _ in range(8):
        num_zeros = int(data[:16], 2)
        reminder_len = delta_length - num_zeros
        reminder = data[16: (16 + reminder_len)]
        encode.append((num_zeros, reminder))
        data = data[(16 + reminder_len):]
    
    zigzag_t = decode_count(encode)
    zigzag = transpose(zigzag_t)
    # link website showing zigzag encoding
    delta = [decode_zigzag(UInt8(int(z, 2))) for z in zigzag]
    original_data = [first_value]
    for i in range(len(delta)):
        data = original_data[i] - delta[i]
        original_data.append(data)
    
    return as_str(original_data)