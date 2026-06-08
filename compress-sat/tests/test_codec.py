from src.codec import UInt8

def test_uint8_init():
    assert UInt8(5)._value == 5
    assert UInt8(-1)._value == 255
    assert UInt8(256)._value == 0

def test_uint8_str():
    assert str(UInt8(5)) == "00000101"
    assert str(UInt8(-1)) == "11111111"
    assert str(UInt8(256)) == "00000000"

def test_uint8_add():
    assert UInt8(5) + UInt8(10) == UInt8(15)
    assert UInt8(250) + UInt8(10) == UInt8(4)