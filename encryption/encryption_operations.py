import json
import math
import random

def gcd(a, h):
    while h:
        a, h = h, a % h
    return a

def generate_keys():
    p = 17093
    q = 16087
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = 17
    while gcd(e, phi) != 1:
        e += 1

    d = modinv(e, phi)
    
    public_key = (e, n)
    private_key = (d, n)
    
    return public_key, private_key

def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

def encrypt(message, public_key):
    e, n = public_key
    return [pow(ord(char), e, n) for char in message]

def decrypt(encrypted_message, private_key):
    values = private_key.strip("()").split(",")
    d = int(values[0])
    n = int(values[1])

    if isinstance(encrypted_message, int):
        decrypted_char = chr(pow(encrypted_message, d, n))
        return decrypted_char
    else:
        raise ValueError("encrypted_message not a number")


def split_file(file_path, segment_size=50):
    with open(file_path, 'rb') as file:
        data = file.read()
    
    return [data[i:i + segment_size] for i in range(0, len(data), segment_size)]

def encrypt_file(file_path, public_key, segment_size=50):
    segments = split_file(file_path, segment_size)
    encrypted_segments = []

    for segment in segments:
        message = segment.decode(errors='ignore')
        encrypted_segments.append(encrypt(message, public_key))

    with open(file_path + '.enc', 'wb') as enc_file:
        for segment in encrypted_segments:
            enc_file.write(bytes(str(segment), 'utf-8'))

    print(f"File {file_path} was encrypted and save as {file_path}.enc")

def decrypt_file(file_path, private_key):
    with open(file_path, 'r') as enc_file:
        segments = json.load(enc_file)

    print(f"segments: {segments}")

    decrypted_segments = []

    for segment in segments:
        decrypted_segments.append(decrypt(segment, private_key))

    print(f"decrypted_segments: {decrypted_segments}")

    combined_content = ''.join(decrypted_segments)

    with open(file_path.replace('.enc', '.dec'), 'wb') as dec_file:
        dec_file.write(combined_content.encode())

    print(f"File {file_path} was decrypted and saved as {file_path.replace('.enc', '')}")

    return combined_content


