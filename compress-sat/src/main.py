import math
import os

from codec import UInt8, as_str, as_uint8, compress, decompress
from download import DW_BANDS
from download import load_dynamic_world
from visualise import plot


if __name__ == "__main__":
    data_dir = "data"

    data = []; original_size = 0
    for file in os.listdir(data_dir):
        pixel_data = load_dynamic_world(os.path.join(data_dir, file))
        original_size += len(pixel_data) * 4  # assumes values take up 4 bytes (32 bits) in memory
        data.append(pixel_data)
    print(f"Original size (float32): {original_size} bytes")

    lossy_data = []; lossy_size = 0
    for pixel_data in data:
        lossy_pixel_data = [UInt8(math.floor(pixel_value*100)) for pixel_value in pixel_data]
        lossy_size += len(pixel_data) * 1  # assumes values take up 1 byte (8 bits) in memory
        lossy_data.append(lossy_pixel_data)
    print(f"Lossy size (uint8): {lossy_size} bytes")

    decompressed_data = []; num_bits = 0
    for pixel_data in lossy_data:
        uncompressed = as_str(pixel_data)
        compressed = compress(uncompressed)
        num_bits += len(compressed)

        decompressed = decompress(compressed)
        assert uncompressed == decompressed
        decompressed_data.append([d._value for d in as_uint8(decompressed)])
    compressed_size = math.ceil(num_bits/8)
    print(f"Compressed size: {compressed_size} bytes")
    print(f"Compression ratio: {original_size / compressed_size:.4f}")

    plot(data, decompressed_data, DW_BANDS)
