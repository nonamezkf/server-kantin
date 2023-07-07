from models import *

# adminsource = [
#     {'role': 'superuser', 'nama': 'admin', 'email': 'kantin@gmail.com ', 'password': '123', 'no_tlp': '081333444555'}
# ]

# for data_dict in adminsource:
#     # Admin diambil dari nama class table 
#     Admin.create(**data_dict)


# pesanansiswa = [
#     {'anak_id': 2, 'totalPembayaran': 5000, 'ttl_pembayaran': '2023-06-21'}
# ]

# for data_dict in pesanansiswa:
#     # Admin diambil dari nama class table 
#     PesananSiswa.create(**data_dict)
orangtua_id = 1

q = Anak.select(Anak.saldo).where(Anak.orangtua_id == orangtua_id)

print(q)