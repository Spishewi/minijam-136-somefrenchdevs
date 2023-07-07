from __future__ import annotations


def tiled_hex_to_rgb(hex: str) -> tuple[int, int, int]:
    r = int(hex[3:5], 16)
    g = int(hex[5:7], 16)
    b = int(hex[7:9], 16)
    return (r, g, b)