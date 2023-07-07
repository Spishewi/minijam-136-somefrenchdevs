def sign(x: int) -> int:
    """
    si positif retourne 1
    si négatif retourne -1
    sinon retourne 0
    """
    if x < 0:
        return -1
    if x > 0:
        return 1
    else:
        return 0
def clamp(val: float, min_val: float, max_val: float) -> float:
        return max(min(val, max_val), min_val)