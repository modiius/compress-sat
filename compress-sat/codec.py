# TODO:
# - change all asserts to raise Exceptions

class UInt8:
    
    def __init__(self, val: int|str):
        """Function initializing the UInt8 class 
        Parameters: 
        val: str or int
            a value that is to be converted into the 8 bit representatio of this number
        """
        # TODO: change the class definition to work also with a str
        self._value = val & 0xFF

    def __str__(self):
        return f"{self._value:08b}"
    
    def __add__(self, other):
        assert isinstance(other, UInt8)
        return UInt8(self._value + other._value)

    def __sub__(self, other):
        assert isinstance(other, UInt8)
        return UInt8(self._value - other._value)

    def __lshift__(self, other):
        assert isinstance(other, UInt8)
        return UInt8(self._value << other._value)
    
    # NOTE: Arithmetic rightshift NOT logical rightshift
    # Insert stack overflow answer here...
    def __rshift__(self, other):
        assert isinstance(other, UInt8)
        if self._value & 2**7 != 0:
            mask = int("1"*other._value + "0"*(8-other._value), 2)
            return UInt8((self._value >> other._value) | mask)
        else:
            return UInt8(self._value >> other._value)
    
    def __xor__(self, other):
        assert isinstance(other, UInt8)
        return UInt8(self._value ^ other._value)
    
    def __invert__(self):
        return UInt8(~self._value)
    
    def __and__(self, other):
        assert isinstance(other, UInt8)
        return UInt8(self._value & other._value)


def as_str(data_uint8: list[UInt8]):
    return "".join([str(d) for d in data_uint8])


def as_uint8(data_str: str):
    assert len(data_str) % 8 == 0
    data_uint8 = []
    for i in range(0, len(data_str), 8):
        value = UInt8(int(data_str[i:i+8], 2))
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
    print(f"ORIGINAL DATA: {[str(og) for og in data_uint8]}")
    first = data_uint8[0]
    delta = [data_uint8[i] - data_uint8[i+1] for i in range(len(data_uint8)-1)]
    print(f"DELTA: {[str(d) for d in delta]}")
    zigzag = [(d<<UInt8(1))^(d>>UInt8(7)) for d in delta]
    print(f"ZIGZAG: {[str(z) for z in zigzag]}")
    zigzag_t = transpose(zigzag)
    encoded_zigzag_t = encode(zigzag_t)
    print(f"TUPLE: {[x for x in encoded_zigzag_t]}")

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


def decompress(data: str):
    delta_length = int(data[:16], 2) - 1    # minus one because the length is smaller by one through the delta (minusing the values from one another)
    first_value = UInt8(int(data[16:24], 2))
    data = data[24:]
    encode = []
    for _ in range(8):
        num_zeros = int(data[:16], 2)
        reminder_len = delta_length - num_zeros
        reminder = data[16: (16 + reminder_len)]
        encode.append((num_zeros, reminder))
        data = data[(16 + reminder_len):]
    
    print(f"TUPLE: {[x for x in encode]}")
    zigzag_t = decode(encode)
    zigzag = transpose(zigzag_t)
    print(f"ZIGZAG: {zigzag}")
    delta = [(UInt8(int(z, 2))>>UInt8(1))^(~(UInt8(int(z, 2))&UInt8(1)) + UInt8(1)) for z in zigzag]
    print(f"DELTA: {[str(d) for d in delta]}")
    original_data = [first_value]
    for i in range(len(delta)):
        data = original_data[i] - delta[i]
        original_data.append(data)
    print(f"ORIGINAL DATA: {[str(og) for og in original_data]}")
    

if __name__ == "__main__":
    import random
    data = [random.choice([UInt8(25),UInt8(24),UInt8(23)]) for _ in range(10)]
    orig = as_str(data)
    compressed = compress(orig)
    print("===================")
    decompress(compressed)