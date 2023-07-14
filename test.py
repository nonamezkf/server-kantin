from datetime import datetime, date, time, timezone

full = datetime.now()

print(f'full = {full}')

d = date.today()

print(f'date = {d}')

# t = time()
# d = date()

# print(f'{d} {t}')


from server import *


last_pesanansiswa = PesananSiswa.select().order_by(PesananSiswa.id.desc()).get()
last_id = last_pesanansiswa.id

print(last_id)

{
	'id_siswa': '1',
	'harga_total': '18000', 
	'detail_pesanan': " 
			{'6': {'harga': 8000, 'kuantitas': 1, 'namaproduk': 'Es Kelapa'}, 
			'7': {'harga': 10000, 'kuantitas': 1, 'namaproduk': 'Kelpon'}}"
}









data = {
    'id_siswa': '1',
    'harga_total': '10000',
    'detail_pesanan': [
        {'harga': 5000, 'kuantitas': 1, 'namaproduk': 'Es Teh'},
        {'harga': 5000, 'kuantitas': 1, 'namaproduk': 'Es Jeruk'}
    ]
}

data_baru = {'harga': 3000, 'kuantitas': 2, 'namaproduk': 'Es Campur'}

for pesanan in data['detail_pesanan']:
    pesanan.update(data_baru)

print(data)


data = {
    'id_siswa': '1',
    'harga_total': '10000',
    'detail_pesanan': [
        {'harga': 5000, 'kuantitas': 1, 'namaproduk': 'Es Teh'},
        {'harga': 5000, 'kuantitas': 1, 'namaproduk': 'Es Jeruk'}
    ]
}

# Data baru yang akan ditambahkan
data_baru = {'harga': 3000, 'kuantitas': 2, 'namaproduk': 'Es Campur'}

# Menambahkan data baru ke setiap dictionary dalam list
for pesanan in data['detail_pesanan']:
    pesanan.update(data_baru)

print(data)