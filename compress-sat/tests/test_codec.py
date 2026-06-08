import random

from src.codec import UInt8, as_str, compress, compress, decompress

def test_uint8_init():
    assert UInt8(5)._value == 5
    assert UInt8(-1)._value == 255
    assert UInt8(256)._value == 0

def test_uint8_str():
    assert str(UInt8(5)) == "00000101"
    assert str(UInt8(-1)) == "11111111"
    assert str(UInt8(256)) == "00000000"


def test_uint8_add():
    assert UInt8(2) + UInt8(3) == UInt8(5)
    assert UInt8(255) + UInt8(1) == UInt8(0)
    assert UInt8(250) + UInt8(10) == UInt8(4)


def test_uint8_sub():
    assert UInt8(10) - UInt8(5) == UInt8(5)
    assert UInt8(0) - UInt8(1) == UInt8(255)
    assert UInt8(5) - UInt8(10) == UInt8(251)


def test_uint8_lshift():
    assert UInt8(1) << UInt8(2) == UInt8(4)
    assert UInt8(255) << UInt8(1) == UInt8(254)
    assert UInt8(0) << UInt8(5) == UInt8(0)


def test_uint8_rshift():
    # Arithmetic right shift operator
    assert UInt8(4) >> UInt8(2) == UInt8(1)
    assert UInt8(255) >> UInt8(1) == UInt8(255)
    assert UInt8(0) >> UInt8(5) == UInt8(0)
    # Logical right shift operator
    assert UInt8(90) @ UInt8(1) == UInt8(45)
    assert UInt8(255) @ UInt8(1) == UInt8(127)
    assert UInt8(0) @ UInt8(5) == UInt8(0)


def test_uint8_xor():
    assert UInt8(5) ^ UInt8(3) == UInt8(6)
    assert UInt8(255) ^ UInt8(0) == UInt8(255)
    assert UInt8(255) ^ UInt8(255) == UInt8(0)


def test_uint8_invert():
    assert ~UInt8(0) == UInt8(255)
    assert ~UInt8(255) == UInt8(0)
    assert ~UInt8(5) == UInt8(250)


def test_uint8_and():
    assert UInt8(5) & UInt8(3) == UInt8(1)
    assert UInt8(255) & UInt8(0) == UInt8(0)
    assert UInt8(255) & UInt8(255) == UInt8(255)


def test_codec():
    random.seed(0)
    for data_size in range(2, 1000, 7):  # datasets of varying size
        data = as_str([random.choice([UInt8(i) for i in range(100)]) for _ in range(data_size)])
        compressed = compress(data)
        decompressed = decompress(compressed)
        assert as_str(data) == decompressed


if __name__ == "__main__":
    test_codec()