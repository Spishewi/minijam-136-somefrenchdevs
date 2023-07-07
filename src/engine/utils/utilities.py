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

def number_to_str(nb:int|float)->str:
    """
    Permet de transformer un entier en string en rajoutant du formatage
    par exemple : 1000 -> 1k
    """
    def only_three_digits(number):
        """
        retourne en nombre contenant trois chiffres au maximum
        """
        if number >= 100:
            return round(number)
        if number >= 10:
            return int(number*10)/10
        return int(number*100)/100

    # On définit les unités
    unities = ["","k","m","b","t","q"]
    for unity in unities:
        if nb < 1000:
            return str(only_three_digits(nb))+unity
        nb = nb/1000
    
    return str(only_three_digits(nb))+"Q"