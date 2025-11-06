import numpy as np
from math import gcd

# ============ Caesar Cipher ============
def caesar_encrypt(text, key):
    result = ""
    for char in text.upper():
        if char.isalpha():
            result += chr(((ord(char) - 65 + key) % 26) + 65)
        else:
            result += char
    return result

def caesar_decrypt(text, key):
    return caesar_encrypt(text, -key)

# ============ Vigenere Cipher ============
def vigenere_encrypt(text, key):
    key = key.upper()
    result = ""
    for i, c in enumerate(text.upper()):
        if c.isalpha():
            shift = ord(key[i % len(key)]) - 65
            result += chr(((ord(c) - 65 + shift) % 26) + 65)
        else:
            result += c
    return result

def vigenere_decrypt(text, key):
    key = key.upper()
    result = ""
    for i, c in enumerate(text.upper()):
        if c.isalpha():
            shift = ord(key[i % len(key)]) - 65
            result += chr(((ord(c) - 65 - shift) % 26) + 65)
        else:
            result += c
    return result

# ============ Affine Cipher ============
def mod_inverse(a, m):
    for i in range(m):
        if (a * i) % m == 1:
            return i
    return None

def affine_encrypt(text, a, b):
    if gcd(a, 26) != 1:
        raise ValueError("a harus relatif prima terhadap 26")
    result = ""
    for char in text.upper():
        if char.isalpha():
            result += chr(((a * (ord(char) - 65) + b) % 26) + 65)
        else:
            result += char
    return result

def affine_decrypt(text, a, b):
    a_inv = mod_inverse(a, 26)
    result = ""
    for char in text.upper():
        if char.isalpha():
            result += chr(((a_inv * ((ord(char) - 65 - b)) % 26) + 65))
        else:
            result += char
    return result

# ============ Playfair Cipher ============
def generate_playfair_matrix(key):
    key = key.upper().replace("J", "I")
    matrix = ""
    for c in key:
        if c not in matrix:
            matrix += c
    for c in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if c not in matrix:
            matrix += c
    return [list(matrix[i:i+5]) for i in range(0, 25, 5)]

def playfair_encrypt(text, key):
    text = text.upper().replace("J", "I").replace(" ", "")
    matrix = generate_playfair_matrix(key)
    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else "X"
        if a == b:
            pairs.append((a, "X"))
            i += 1
        else:
            pairs.append((a, b))
            i += 2

    result = ""
    for a, b in pairs:
        ax, ay, bx, by = -1, -1, -1, -1
        for r in range(5):
            for c in range(5):
                if matrix[r][c] == a:
                    ax, ay = r, c
                if matrix[r][c] == b:
                    bx, by = r, c
        if ax == bx:
            result += matrix[ax][(ay+1)%5] + matrix[bx][(by+1)%5]
        elif ay == by:
            result += matrix[(ax+1)%5][ay] + matrix[(bx+1)%5][by]
        else:
            result += matrix[ax][by] + matrix[bx][ay]
    return result

# ============ Hill Cipher ============
def hill_encrypt(text, key_matrix):
    n = len(key_matrix)
    text = text.upper().replace(" ", "")
    while len(text) % n != 0:
        text += "X"
    result = ""
    for i in range(0, len(text), n):
        block = [ord(c) - 65 for c in text[i:i+n]]
        enc = np.dot(key_matrix, block) % 26
        result += ''.join(chr(e + 65) for e in enc)
    return result

# ============ Menu Program ============
def main():
    while True:
        print("\n=== PROGRAM KRIPTOGRAFI KLASIK ===")
        print("1. Caesar Cipher")
        print("2. Vigenere Cipher")
        print("3. Affine Cipher")
        print("4. Playfair Cipher")
        print("5. Hill Cipher")
        print("0. Keluar")
        pilihan = input("Pilih algoritma: ")

        if pilihan == "1":
            teks = input("Masukkan teks: ")
            key = int(input("Masukkan key (angka): "))
            enc = caesar_encrypt(teks, key)
            print("Ciphertext:", enc)
            print("Dekripsi :", caesar_decrypt(enc, key))

        elif pilihan == "2":
            teks = input("Masukkan teks: ")
            key = input("Masukkan key (kata): ")
            enc = vigenere_encrypt(teks, key)
            print("Ciphertext:", enc)
            print("Dekripsi :", vigenere_decrypt(enc, key))

        elif pilihan == "3":
            teks = input("Masukkan teks: ")
            a = int(input("Masukkan a: "))
            b = int(input("Masukkan b: "))
            enc = affine_encrypt(teks, a, b)
            print("Ciphertext:", enc)
            print("Dekripsi :", affine_decrypt(enc, a, b))

        elif pilihan == "4":
            teks = input("Masukkan teks: ")
            key = input("Masukkan key (kata): ")
            enc = playfair_encrypt(teks, key)
            print("Ciphertext:", enc)

        elif pilihan == "5":
            teks = input("Masukkan teks (panjang kelipatan 2): ")
            print("Gunakan matriks kunci [[3,3],[2,5]] (contoh)")
            key_matrix = np.array([[3, 3], [2, 5]])
            enc = hill_encrypt(teks, key_matrix)
            print("Ciphertext:", enc)

        elif pilihan == "0":
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()
