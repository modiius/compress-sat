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
    """Function translating a list of UInt8 values into a one string representation of thouse values.
    
    Parameters
    ----------
     - data_uint8: list[UInt8]
        a list of UInt8 values
        
    Returns
    -------
     - concatinate string representation of the values 
     
    Exaple
    >>> as_str([UInt8(2), UInt8(5)])
    '0000001000000101'
    >>> as_str([UInt8(1)])
    '00000001'
    >>> as_str([UInt8(3), UInt8(1), UInt8(25)])
    '000000110000000100011001'
    """
    return "".join([str(d) for d in data_uint8])


def as_uint8(data_str: str):
    """Function splitting a string representatio of many UInt8 vlues into the consecutive UInt8 values.
    
    Parameters
    ----------
     - data_str: str
        the string of 1 and 0 representing UInt8 values
        
    Returns
    -------
     - data_uint8: list[UInt8]
        a list of UInt8 values extracted form the string
    
    Example
    -------
    >>> as_uint8('000000110000000100011001')
    '[<codec.UInt8 object at 0x000001FBF747E5F0>, <codec.UInt8 object at 0x000001FBF74DD980>, <codec.UInt8 object at 0x000001FBF7520050>]'
    """
    if len(data_str) % 8 != 0:
        raise LengthError(data_str)
    data_uint8 = []
    for i in range(0, len(data_str), 8):
        value = UInt8(data_str[i:i+8])
        data_uint8.append(value)
    
    return data_uint8


def transpose(data: list) -> list[str]:
    """Function that transposes a list of elements. The elements of that list have to have the same length. 
    
    The function returns a list thats length is equal to the original list element length. The elements of the transposed list have the same length as the original list length.

    Parameters
    ----------
     - data: list
        list of same length elements
    
    Returns
    -------
     - data_t: list
        list of transposed values
    
    Example
    -------
    >>> transpose([UInt8(1), UInt8(0)])
    ['00', '00', '00', '00', '00', '00', '00', '10']
    >>> transpose(['00', '00', '00', '00', '00', '00', '00', '10'])
    ['00000001', '00000000']
    >>> transpose(['red', 'red'])
    ['rr', 'ee', 'dd']
    """
    
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
    """Function that takes in a list of strings and returns a tuple containig the count of zeros at the beggining of every element of the list and the remaining part of this element.
     
    Parameters
    -----------
     - data_str: list[str]
        the list of strings
    
    Returns
    -------
     - data_tuple: list[tuple(int, str)]
        the list of tuples consisting of the amout of zeros andthe remining string value 
    
    Example
    -------
    >>> encode_count(['000001011', '0010101', '000000'])
    [(5, '1011'), (2, '10101'), (6, '')]
    >>> encode_count(['000001', '00001100', '0000000']) 
    [(5, '1'), (4, '1100'), (7, '')]
    """
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
    """Fuction that performes zigzag encoding on the UInt8 values. 

    Based on: https://gist.github.com/mfuerstenau/ba870a29e16536fdbaba.
    
    Zigzag encoding maps the negative numbers in the UInt8 representation to positive number representations (-1 becomes 1, 1 becomes 2, -2 becomes 3 and so on...).
    All the positive values are represented by even numbers (their double values) and all of the negative values are represented by uneven numbers (their double absolute value minus 1).

    Parameters
    ----------
     - n: UInt8
        the UInt8 value to be encoded
    
    Returns
    -------
     - UInt8 
        encoded value
    
    Example
    -------
    >>> str(UInt8(1)) 
    '00000001'
    >>> str(encode_zigzag(UInt8(1)))   
    '00000010'
    >>> str(UInt8(-1))
    '11111111'
    >>> str(encode_zigzag(UInt8(-1)))
    '00000001'
    >>> str(UInt8(-2))
    '11111110'
    >>> str(encode_zigzag(UInt8(-2)))
    '00000011'
    """
    return (n << UInt8(1)) ^ (n >> (k - UInt8(1)))


def compress(data: str):
    """Function performing the compression of a string of data.
    
    Function devides the string into UInt8 values and saves the first value. Calculates the differences between each datapoint and it's next neighbour, resoulting in the length of the list of data being one smaller than at the begining.
    The substraction of values and the zigzag encoding is used to maximize the amount of zeros at the begenning of each row, as they are the elemet to be compressed.
    
    Parameters
    ----------
     - data: str
        the string of 1 and 0 
    
    Returns
    -------
     - result: str
        a string which first 16 bits encode the length of the original data list, the next 8 bits encode the first value from the dataset. The rest of the result is the amount of zeros (encoded in 16 bit value) and the remainder for each of the transposed data values.
        
    Example
    -------
    >>> compress('0000000100000111000000100000000000000011')                
    '0000000000000101000000010000000000000100000000000000010000000000000001000000000000000100000000000000000011000000000000000010110000000000000000110000000000000000001001'
    This compression works best for big datasets, for small ones its very inefficient.
    """
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
    """Function that decoded the tuple of the value of zeroes and the remaining string into a list of strings.
    
    *This function does the opposite to the "encode_count" function.

    Parameters
    ----------
     - data: list[touple(int, str)]
        list of touples 
    
    Returns
    -------
     - data_str: list[str]
        list of strings 
    
    Example
    -------
    >>> decode_count([(4, '1110'), (2, '101011'), (7, '1'),(8, '')])
    ['00001110', '00101011', '00000001', '00000000']
    >>> decode_count([(5, '10'), (2, '1010101'), (4, 'red')])
    ['0000010', '001010101', '0000red']
    """
    data_str = []
    for num_zeros, reminder in data:
        zeros = '0' * num_zeros
        data_str.append(zeros + reminder)

    return data_str


def decode_zigzag(n: UInt8):
    """Fuction that reverses the zigzag encoding on the UInt8 value. 
    
    Based on: https://gist.github.com/mfuerstenau/ba870a29e16536fdbaba.

    Parameters
    ----------
     - n: UInt8
        value to be decoded
    
    Returns
    -------
     - UInt8
        the decoded value

    Example
    -------
    >>> str(UInt8(-1))
    '11111111'
    >>> str(encode_zigzag(UInt8(-1)))
    '00000001'
    >>> str(decode_zigzag(encode_zigzag(UInt8(-1))))
    '11111111'
    """
    return (n @ UInt8(1)) ^ (~(n & UInt8(1)) + UInt8(1))


def decompress(data: str) -> str:
    """This function performes decompression on a compressed dataset. It's a reverse of the compress function. 
    
    First it finds the length of data and the first value as the first 16 and 8 bits of the original data string. Then it devides the remaining dataset into 16 bit information about the amout of zeros and the remainders from the 8 bit representations of the values to later preform decoding.
    The data is then transposed the zigzag encoding is decoded and the delta calculation id reversed.
    
    Parameters
    ----------
     - data: str
        a string of data from the compression algorithm
    
    Returns
    -------
     - str
        the original data string
    
    Example
    -------
    >>> decompress('0000000000000101000000010000000000000100000000000000010000000000000001000000000000000100000000000000000011000000000000000010110000000000000000110000000000000000001001')
    '0000000100000111000000100000000000000011'
    """
    # minus one because the length of the list of data is smaller by one through the delta (substracting the values from one another)
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