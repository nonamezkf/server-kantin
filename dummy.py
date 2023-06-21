# from db import *

# adminsource = [
#     {'role': 'superuser', 'nama': 'admin', 'email': 'kantin@gmail.com ', 'password': '123', 'no_tlp': '081333444555'}
# ]

# for data_dict in adminsource:
#     # Admin diambil dari nama class table 
#     Admin.create(**data_dict)

import random
import string

def generate_token(length):
    # Menggabungkan karakter huruf besar, huruf kecil, dan angka
    characters = string.ascii_letters + string.digits
    
    # Mengacak urutan karakter untuk membuat string acak
    token = ''.join(random.choice(characters) for i in range(length))
    
    return token

# Contoh pemanggilan fungsi untuk membuat token dengan panjang 10 karakter
token = generate_token(10)
print(token)