class UInt8:
    """ A class representaing a data type value as an unsigned int8.

    Attributes:
    -----------
     - val: int|str
            the value of the number to be converted into UInt8
    
    Methods:
    -----------
     - __str__ 
     - __add__
     - __sub__
     - __lshift__
     - __rshift__
     - __xor__
     - __invert__
     - __and__
    """
    def __init__(self, val: int|str):
        """Function initializing the UInt8 class 
        
        Parameters: 
        val: str or int
            a value that is to be converted into its 8 bit representation
        """
        if isinstance(val, str):
            if len(val) != 8:
                raise ValueError(f'Expected length is divisible by 8 and a string of len={len(val)} was given.')
            self._value = int(val, 2) & 0xFF
        else:
            self._value = val & 0xFF
    
    def __eq__(self, other):
        assert isinstance(other, UInt8)
        return self._value == other._value

    def __str__(self):
        return f"{self._value:08b}"
    
    def __add__(self, other):
        if not isinstance(other, UInt8):
            raise TypeError(f'Expected type is UInt8 and a {type(other)} was given.')
        
        return UInt8(self._value + other._value)

    def __sub__(self, other):
        if not isinstance(other, UInt8):
            raise TypeError(f'Expected type is UInt8 and a {type(other)} was given.')
        
        return UInt8(self._value - other._value)

    def __lshift__(self, other):
        if not isinstance(other, UInt8):
            raise TypeError(f'Expected type is UInt8 and a {type(other)} was given.')
        
        return UInt8(self._value << other._value)
    
    # NOTE: Arithmetic rightshift NOT logical rightshift
    # Insert stack overflow answer here...
    def __rshift__(self, other):
        if not isinstance(other, UInt8):
            raise TypeError(f'Expected type is UInt8 and a {type(other)} was given.')
        
        if self._value & 2**7 != 0:
            mask = int("1"*other._value + "0"*(8-other._value), 2)
            return UInt8((self._value >> other._value) | mask)
        else:
            return UInt8(self._value >> other._value)
    
    def __xor__(self, other):
        if not isinstance(other, UInt8):
            raise TypeError(f'Expected type is UInt8 and a {type(other)} was given.')
        
        return UInt8(self._value ^ other._value)
    
    def __invert__(self):
        return UInt8(~self._value)
    
    def __and__(self, other):
        if not isinstance(other, UInt8):
            raise TypeError(f'Expected type is UInt8 and a {type(other)} was given.')
        
        return UInt8(self._value & other._value)


def as_str(data_uint8: list[UInt8]):
    return "".join([str(d) for d in data_uint8])


def as_uint8(data_str: str):
    if len(data_str) % 8 != 0:
        raise ValueError(f'Expected length is divisible by 8 and not len={len(data_str)}.')
    data_uint8 = []
    for i in range(0, len(data_str), 8):
        value = UInt8(data_str[i:i+8])
        data_uint8.append(value)
    
    return data_uint8


def transpose(data: list) -> list[str]:
    data_t = []
    for pos in range(len(str(data[0]))): 
        row_t = ""
        for i in range(len(data)):
            row_t += str(data[i])[pos]
        data_t.append(row_t)
    
    return data_t


def encode(data_str: list[str]) -> tuple[int, str]:
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


def compress(data: str):
    data_uint8 = as_uint8(data)
    first = data_uint8[0]
    delta = [data_uint8[i] - data_uint8[i+1] for i in range(len(data_uint8)-1)]
    zigzag = [(d<<UInt8(1))^(d>>UInt8(7)) for d in delta]
    zigzag_t = transpose(zigzag)
    encoded_zigzag_t = encode(zigzag_t)

    result = f"{len(data_uint8):016b}{str(first)}"
    for num_zeros, remainder in encoded_zigzag_t:
        result = result + f"{num_zeros:016b}" + remainder

    return result


def decode(data: list[tuple[int, str]]):
    data_str = []
    for num_zeros, reminder in data:
        zeros = '0' * num_zeros
        data_str.append(zeros + reminder)

    return data_str


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
    
    zigzag_t = decode(encode)
    zigzag = transpose(zigzag_t)
    # link website showing zigzag encoding
    delta = [(UInt8(z)>>UInt8(1))^(~(UInt8(z)&UInt8(1)) + UInt8(1)) for z in zigzag]
    original_data = [first_value]
    for i in range(len(delta)):
        data = original_data[i] - delta[i]
        original_data.append(data)
    
    return as_str(original_data)