import os
import numpy as np
import math
import cv2
import random
import json
from pathlib import Path

def is_prime(number):
    if number <= 1:
        return False
    for i in range(2, int(math.sqrt(number)) + 1):
        if number % i == 0:
            return False
    return True

def generate_primes():
    while True:
        prime1 = random.randint(100, 1000)
        prime2 = random.randint(100, 1000)
        if is_prime(prime1) and is_prime(prime2) and prime1 != prime2:
            return prime1, prime2

def generate_E(m):
    coprime_number = 2
    while math.gcd(m, coprime_number) != 1:
        coprime_number = random.randint(2, m - 1)
    return coprime_number

def generate_D(M, E):
    k = 1
    while True:
        d = (((M * k) + 1) / E)
        if d.is_integer():
            return int(d)
        k += 1

def generate_key_pair():
    p, q = generate_primes()
    n = p * q
    m = (p - 1) * (q - 1)
    e = generate_E(m)
    d = generate_D(m, e)
    return (e, n), (d, n)

def encrypt(data, public_key):
    e, n = public_key
    return [pow(int(char), e, n) for char in data]

def decrypt(encrypted_data, private_key):
    if isinstance(private_key, str):
        private_key = eval(private_key)
    d, n = private_key
    return [pow(char, d, n) for char in encrypted_data]

def split_data(data, segment_size=50):
    return [data[i:i + segment_size] for i in range(0, len(data), segment_size)]

def encrypt_file(file_path, public_key, segment_size=50):
    file_path = Path(file_path)
    data = None

    if file_path.suffix in ['.jpg', '.png', '.bmp']:
        img = cv2.imread(str(file_path))
        height, width = img.shape[:2]
        data = img.flatten().astype(np.uint8)
    else:
        with open(file_path, 'rb') as file:
            data = file.read()

    segments = split_data(data, segment_size)
    encrypted_segments = [encrypt(segment, public_key) for segment in segments]

    encrypted_file_path = file_path.with_name(file_path.name + '.enc')

    with open(encrypted_file_path, 'w') as enc_file:
        json.dump({
            "segments": encrypted_segments,
            "metadata": {
                "type": "image" if file_path.suffix in ['.jpg', '.png', '.bmp'] else "text",
                "height": height if 'height' in locals() else None,
                "width": width if 'width' in locals() else None,
            }
        }, enc_file)

    print(f"Fișierul {file_path} a fost criptat și salvat ca {encrypted_file_path}")
    return str(encrypted_file_path) 


def decrypt_file(file_path, private_key):
    file_path = Path(file_path)
    with open(file_path, 'r') as enc_file:
        encrypted_data = json.load(enc_file)

    encrypted_segments = encrypted_data["segments"]
    metadata = encrypted_data["metadata"]

    decrypted_segments = []
    for segment in encrypted_segments:
        decrypted_segments.extend(decrypt(segment, private_key))

    if metadata["type"] == "image":
        flat_array = np.clip(np.array(decrypted_segments), 0, 255).astype(np.uint8)
        img = flat_array.reshape(metadata["height"], metadata["width"], 3)
        
        original_extension = file_path.suffix
        output_path = file_path.stem
        cv2.imwrite(str(Path(output_path).with_suffix(original_extension)), img)
        print(f"Imaginea {file_path} a fost decriptată și salvată ca {output_path}{original_extension}")
        
        os.startfile(str(Path(output_path).with_suffix(original_extension)))
    else:
        output_path = file_path.stem
        with open(output_path, 'wb') as dec_file:
            dec_file.write(bytes(decrypted_segments))
        print(f"Fișierul text {file_path} a fost decriptat și salvat ca {output_path}")
        
        if os.name == 'nt':
            os.startfile(output_path)
        elif os.name == 'posix':
            subprocess.call(['open', output_path])
