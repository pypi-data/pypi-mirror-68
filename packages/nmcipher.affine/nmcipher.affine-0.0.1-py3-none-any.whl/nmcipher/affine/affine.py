from math import gcd

class Affine():

    @staticmethod
    def find_modular_inverse(a, m):
        if gcd(a, m) != 1:
            return None
        u1, u2, u3 = 1, 0, a
        v1, v2, v3 = 0, 1, m
        while v3 != 0:
            q = u3 // v3
            v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
        return u1 % m

    def __init__(self, key, symbols):
        keyA, keyB = key // len(symbols), key % len(symbols) 
        if keyA == 1:
            raise ValueError("Key is weak when key A = 1")
        if keyB == 0:
            raise ValueError("Key is weak when key B = 0")
        if gcd(keyA, len(symbols)) != 1:
            raise ValueError(f"Multiplicative key ({keyA}) and length of symbols ({len(symbols)}) must be co-prime")

        self._translation_table = str.maketrans({symbols[i]: symbols[(i * keyA + keyB) % len(symbols)] for i in range(len(symbols))})

        keyA_inverse = self.find_modular_inverse(keyA, len(symbols))
        self._reverse_translation_table = str.maketrans({symbols[i]: symbols[((i - keyB) * keyA) % len(symbols)] for i in range(len(symbols))})

    def encrypt(self, message):
        return message.translate(self._translation_table)

    def decrypt(self, message):
        return message.translate(self._reverse_translation_table)
