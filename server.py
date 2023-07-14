from flask import Flask, jsonify, session
from peewee import *
from flask_restful import Resource, Api, reqparse
from hashlib import sha256

import datetime
from datetime import date
import ast

import sqlite3

from peewee import *

import pd

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'LKANCNHkjhasd123hb34gv5y3245vu2vvd'

DATABASE = SqliteDatabase('dummy.db')

class BaseModel(Model):
	class Meta:
		database = DATABASE

class OrangTua(BaseModel):
	username = CharField(unique=True)
	password = CharField()
	role = TextField()
	nama = TextField()
	ttl = DateField('%d-%m-%Y')
	alamat = TextField()
	email = CharField()
	no_tlp = CharField()
	join_at = DateTimeField(default=datetime.datetime.now())

class Anak(BaseModel):
	orangtua_id = ForeignKeyField(OrangTua, backref='anaks')
	nama = TextField()
	username = CharField()
	role = TextField()
	password = CharField()
	kelas = CharField()
	alamat = TextField()
	no_tlp = CharField()
	saldo = IntegerField()
	tgl_lahir = DateField()

class Admin(BaseModel):
	role = TextField()
	nama = TextField()
	email = CharField()
	password = CharField()
	no_tlp = CharField()

class Karyawan(BaseModel):
	admin_id = ForeignKeyField(Admin, backref='karyawans')
	nama = TextField()
	email = CharField()
	password = CharField()
	no_tlp = CharField()

class PesananSiswa(BaseModel):
	anak_id = ForeignKeyField(Anak, backref='pesanansiswas')
	totalPembayaran = IntegerField()
	ttl_pemesanan = DateTimeField(default=datetime.date.today())

class DetailPesanan(BaseModel):
	pesanansiswa_id = ForeignKeyField(PesananSiswa, backref='detailpesanan')
	kuantitas = CharField()
	harga = IntegerField()
	namaproduk = TextField()

def create_tables():
    with database:
        database.connect()
        database.create_tables([OrangTua, Anak, Admin, Karyawan, PesananSiswa, DetailPesanan])
        database.close()


# database.connect()
# database.create_tables([OrangTua, Anak, Admin, Karyawan, PesananSiswa, DetailPesanan])




# ############## function ###############

# def auth_user_admin(admin):
# 	session['admin_id'] = admin.id
	# print(session['admin_id'])




# #################### Resources #####################

# Resourcer Api login admin
class Loginadmin(Resource):
    # login admin
	def post(self):
		parserData = reqparse.RequestParser()
		parserData.add_argument('username')
		parserData.add_argument('password')

		parserAmbilData = parserData.parse_args()
		form_username = parserAmbilData.get('username')
		form_password = parserAmbilData.get('password')

		try :
			hash_password = sha256(form_password.encode('utf-8')).hexdigest()
			admin = Admin.get((Admin.nama == form_username) & (Admin.password == hash_password))
		except Admin.DoesNotExist:
			return {"message":"gagal"}
		else:
			admin_id = session['admin_id'] = admin.id
			auth_user = {
				"admin_id": admin_id
			}

			# print(auth_user)
			# auth_user_admin(admin)
			# print(session['admin_id'])
			# result = "sukses"
			return {"message":"sukses", "auth_user":auth_user}

# Resource Api logout admin
class logout(Resource):
	def get(self):
		parserData = reqparse.RequestParser()
		parserData.add_argument('session_hapus')
		parserAmbilData = parserData.parse_args()
		hapus_session = parserAmbilData.get('session_hapus')

		if hapus_session == True:
			session.pop('admin_id', None)

# Resource Semua Data Karyawan
class Karyawans(Resource):
	def get(self):
		query = Karyawan.select()
		datas = []
		# num = 0
		for row in query:
			datas.append({
				'id':row.id,
				'nama':row.nama,
				'email':row.email,
				'no_tlp': row.no_tlp
			})

		return jsonify(datas)


	def post(self):
		parserData = reqparse.RequestParser()
		parserData.add_argument('id_admin')
		parserData.add_argument('nama')
		parserData.add_argument('email')
		parserData.add_argument('no_tlp')
		parserData.add_argument('password')

		parserAmbilData = parserData.parse_args()
		id_admin = parserAmbilData.get('id_admin')
		form_nama = parserAmbilData.get('nama')
		form_email = parserAmbilData.get('email')
		form_no_tlp = parserAmbilData.get('no_tlp')
		form_password = parserAmbilData.get('password')

		save = Karyawan.create(
			admin_id = id_admin,
			nama = form_nama,
			email = form_email,
			no_tlp = int(form_no_tlp),
			password = form_password
		)


# Resource Data update Karyawan Berdasarkan Id karyawan
class Karyawanbyid(Resource):
	def get(self,id):
		
		query = Karyawan.select().where(Karyawan.id == id)
		datas = []

		for row in query:
			datas.append({
				'id':row.id,
				'nama':row.nama,
				'email':row.email,
				'no_tlp':row.no_tlp,
			})

		return jsonify(datas)


	def put(self, id):

		parserData = reqparse.RequestParser()
		parserData.add_argument('id_admin')
		parserData.add_argument('nama')
		parserData.add_argument('email')
		parserData.add_argument('no_tlp')
		parserData.add_argument('password')

		parserAmbilData = parserData.parse_args()
		id_admin = parserAmbilData.get('id_admin')
		form_nama = parserAmbilData.get('nama')
		form_email = parserAmbilData.get('email')
		form_no_tlp = parserAmbilData.get('no_tlp')
		form_password = parserAmbilData.get('password')

		query = Karyawan.update({Karyawan.admin_id:id_admin, Karyawan.nama:form_nama, Karyawan.email:form_email, Karyawan.no_tlp:form_no_tlp, Karyawan.password:form_password,}).where(Karyawan.id == id)
		query.execute()

	def delete(self, id):
		query = Karyawan.delete().where(Karyawan.id == id)
		query.execute()


# Resource Api login Karyawan
class Loginkaryawan(Resource):

	def post(self):
		parserData = reqparse.RequestParser()
		parserData.add_argument('email')
		parserData.add_argument('password')

		parserAmbilData = parserData.parse_args()
		form_email = parserAmbilData.get('email')
		form_password = parserAmbilData.get('password')

		try :
			hash_password = sha256(form_password.encode('utf-8')).hexdigest()
			karyawan = Karyawan.get((Karyawan.email == form_email) & (Karyawan.password == hash_password))
		except Karyawan.DoesNotExist:
			return {"message":"gagal"}
		else:
			karyawan_id = session['karyawan_id'] = karyawan.id
			print(karyawan_id)
			auth_karyawan = {
				"karyawan_id": karyawan_id
			}

			# print(auth_user)
			# auth_user_admin(admin)
			# print(session['admin_id'])
			# result = "sukses"
			return {"message":"sukses", "auth_karyawan":auth_karyawan}

	    # parserData = reqparse.RequestParser()
		# parserData.add_argument('username')
		# parserData.add_argument('password')

		# parserAmbilData = parserData.parse_args()
		# form_username = parserAmbilData.get('username')
		# form_password = parserAmbilData.get('password')

		# try :
		# 	hash_password = sha256(form_password.encode('utf-8')).hexdigest()
		# 	admin = Admin.get((Admin.nama == form_username) & (Admin.password == hash_password))
		# except Admin.DoesNotExist:
		# 	return {"message":"gagal"}
		# else:
		# 	admin_id = session['admin_id'] = admin.id
		# 	auth_user = {
		# 		"admin_id": admin_id
		# 	}

		# 	# print(auth_user)
		# 	# auth_user_admin(admin)
		# 	# print(session['admin_id'])
		# 	# result = "sukses"
		# 	return {"message":"sukses", "auth_user":auth_user}


class SearchHistoriPesanan(Resource):
	def get(self):
		parserData = reqparse.RequestParser()
		parserData.add_argument('forminput')

		parserAmbilData = parserData.parse_args()
		form_input = parserAmbilData.get('forminput')

		query = PesananSiswa.select().where(PesananSiswa.id == form_input)

		datas = []

		for row in query:
			datas.append({
				'id':row.id,
				'totalPembayaran':row.totalPembayaran,
				'ttl_pemesanan':row.ttl_pemesanan.strftime("%d/%B/%Y")
			})
		return jsonify(datas)


# Resource Api logout Karyawan
class Logoutkaryawan(Resource):
	def get(self):
		parserData = reqparse.RequestParser()
		parserData.add_argument('session_hapus')
		parserAmbilData = parserData.parse_args()
		hapus_session = parserAmbilData.get('session_hapus')

		if hapus_session == True:
			session.pop('karyawan_id', None)

global orangtua_id_session

# Resource Api login orang tua
class Loginorangtua(Resource):

	def post(self):
		parserData = reqparse.RequestParser()
		parserData.add_argument('username')
		parserData.add_argument('password')

		parserAmbilData = parserData.parse_args()
		form_username = parserAmbilData.get('username')
		form_password = parserAmbilData.get('password')

		try :
			hash_password = sha256(form_password.encode('utf-8')).hexdigest()
			orangtua = OrangTua.get((OrangTua.username == form_username) & (OrangTua.password == hash_password))
		except OrangTua.DoesNotExist:
			return {"message":"gagal"}
		else:
			session['orangtua_id'] = orangtua.id
			orangtua_id_session = session['orangtua_id']
			# print(orangtua_id_session)
			auth_orangtua = {
				"orangtua_id": orangtua_id_session
			}

			# print(auth_user)
			# auth_user_admin(admin)
			# print(session['admin_id'])
			# result = "sukses"
			return {"message":"sukses", "auth_orangtua":auth_orangtua}


# Resource Api logout orang tua
class Logoutorangtua(Resource):
	def get(self):
		parserData = reqparse.RequestParser()
		parserData.add_argument('session_hapus')

		parserAmbilData = parserData.parse_args()
		hapus_session = parserAmbilData.get('session_hapus')

		if hapus_session == True:
			session.pop('orangtua_id', None)


# Resource Histori Semua pesanan anak berdasarkan id orang tua
class Historipesanan(Resource):
	def get(self, orangtua_id):
		query = PesananSiswa.select().join(Anak).where(Anak.orangtua_id == orangtua_id)
		# query = ''
		datas = []
		for row in query:
			datas.append({
				'id':row.id,
				'totalPembayaran':row.totalPembayaran,
				'ttl_pemesanan':row.ttl_pemesanan.strftime("%d/%B/%Y")
			})
		return jsonify(datas)


class Totalsaldoanaks(Resource):
	def get(self, orangtua_id):
		totalsaldo = Anak.select(fn.SUM(Anak.saldo)).where(Anak.orangtua_id == orangtua_id).scalar()
		# q = query.order_by(SQL('sld'))
		# datas = []
		# for row in query:
		# 	datas.append({
		# 		'saldo':row.sld,
		# 	})
		# jsonify(datas)

		return {'messages': totalsaldo}

class Totalpembelians(Resource):
	def get(self, orangtua_id):
		totalpembelian = PesananSiswa.select().join(Anak).where(Anak.orangtua_id == orangtua_id).count()

		return {'messages' : totalpembelian}


class NamaAnak(Resource):
	def get(self, orangtua_id):
		query = Anak.select(Anak.nama).where(Anak.orangtua_id == orangtua_id)

		datas = []
		for row in query:
			datas.append({
				'nama' : row.nama
				})	

		return jsonify(datas)

class SearchDataByName(Resource):
	def get(self, orangtua_id):
		parserData = reqparse.RequestParser()
		parserData.add_argument('formoption')

		parserAmbilData = parserData.parse_args()
		form_option = parserAmbilData.get('formoption')

		# query untuk menampilkan histori pesanan berdasarkan nama anak
		queryHistoriPesanan = PesananSiswa.select().join(Anak).where(Anak.orangtua_id == orangtua_id, Anak.nama.contains(form_option) )
		datas = []
		for row in queryHistoriPesanan:
			datas.append({
				'id':row.id,
				'totalPembayaran':row.totalPembayaran,
				'ttl_pemesanan':row.ttl_pemesanan.strftime("%d/%B/%Y")
			})

		# query untuk menampilkan total pembelian
		totalpembelian = PesananSiswa.select().join(Anak).where(Anak.orangtua_id == orangtua_id, Anak.nama.contains(form_option)).count()

		# query untuk menampilkan total saldo
		totalsaldo = Anak.select(Anak.saldo).where(Anak.orangtua_id == orangtua_id, Anak.nama.contains(form_option)).scalar()


		# tampilkan nama

		queryNama = Anak.select(Anak.nama).where(Anak.nama.contains(form_option), Anak.orangtua_id == orangtua_id)

		namanya = []
		for row in queryNama:
			namanya.append({
				"nama" : row.nama
				})

		return {"data" : datas, "totalpembelian" : totalpembelian, "totalsaldo" : totalsaldo, "namanya" : namanya}



class Detailpesanan(Resource):
	def get(self, id_pesanan):
		# query menampilkan detail pesanan
		query = DetailPesanan.select().join(PesananSiswa).where(DetailPesanan.pesanansiswa_id == id_pesanan)
		datas = []
		for row in query:
			datas.append({
				'namaproduk':row.namaproduk,
				'kuantitas': row.kuantitas,
				'harga': row.harga
				})

		# query menampilkan nama
		queryNama = Anak.select(Anak.nama).join(PesananSiswa).where(PesananSiswa.anak_id == Anak.id, PesananSiswa.id == id_pesanan)
		namanya = []
		for row in queryNama:
			namanya.append({
				"nama" : row.nama
				})

		# query menampilkan tanggal
		queryTanggal = PesananSiswa.get(PesananSiswa.id == id_pesanan).ttl_pemesanan.strftime("%d/%B/%Y")

		queryTotalPembelian = PesananSiswa.get(PesananSiswa.id == id_pesanan).totalPembayaran



		return {"detail" : datas, "namanya": namanya, "ttl_pemesanan":queryTanggal, "totalPembayaran":queryTotalPembelian}

class Dataanak(Resource):
	def get(self, orangtua_id):
		query = Anak.select().where(Anak.orangtua_id == orangtua_id)

		datas = []

		for data in query:
			datas.append({
				"nama":data.nama,
				"saldo":data.saldo,
				"alamat":data.alamat,
				"kelas" : data.kelas,
				"tgl_lahir":data.tgl_lahir.strftime("%d/%B/%Y")
				})

		return {"datas" : datas}

class Dataorangtua(Resource):
	def get(self, orangtua_id):
		query = OrangTua.select().where(OrangTua.id == orangtua_id)
		datas = []
		for data in query:
			datas.append({
				"nama":data.nama,
				"alamat":data.alamat,
				"ttl": data.ttl,
				"no_tlp" : data.no_tlp,
				"email" : data.email
				})
		return jsonify(datas)


class SemuaHistoriPesanan(Resource):
	def get(self):
		query = PesananSiswa.select().order_by(PesananSiswa.ttl_pemesanan.desc())
		datas = []
		for row in query:
			datas.append({
				'id':row.id,
				'totalPembayaran':row.totalPembayaran,
				'ttl_pemesanan':row.ttl_pemesanan.strftime("%d/%B/%Y")
			})
		return jsonify(datas)


class Product(Resource):
	def get(self):
		rows = pd.products.select()
		datas=[]
		for row in rows:
			datas.append({
				'id':row.id,
				'name':row.name,
				'desc':row.desc,
				'price':row.price,
				'quantity':row.quantity,
				'category':row.category,
				'image':row.image
			})
		return jsonify(datas)



class ProductSearch(Resource):
	def get(self):
		parserData = reqparse.RequestParser()
		parserData.add_argument('formoption')

		parserAmbilData = parserData.parse_args()
		form_option = parserAmbilData.get('formoption')

		rows = pd.products.select().where(pd.products.category.contains(form_option))

		datas=[]
		for row in rows:
			datas.append({
				'id':row.id,
				'name':row.name,
				'desc':row.desc,
				'price':row.price,
				'quantity':row.quantity,
				'category':row.category,
				'image':row.image
			})

		return jsonify(datas)



class Getproductbyid(Resource):
	def get(self, product_id):

		nama = pd.products.get(pd.products.id == product_id).name
		harga =  pd.products.get(pd.products.id == product_id).price
		last_pesanansiswa = PesananSiswa.select().order_by(PesananSiswa.id.desc()).get().id

		
		# harga = query.price
		# datas = []

		# for row in query :
		# 	datas.append({
		# 		'name':row.name,
		# 		'harga':row.price
		# 		})

		return {"nama":nama, "harga":harga, "pesanansiswa_id":last_pesanansiswa}





class Order(Resource):
	def post(self):
		parserData = reqparse.RequestParser()
		parserData.add_argument('id_siswa')
		parserData.add_argument('harga_total')
		parserData.add_argument('detail_pesanan')


		parserAmbilData = parserData.parse_args()
		id_siswa = parserAmbilData.get('id_siswa')
		harga_total = parserAmbilData.get('harga_total')
		detail_pesanan = parserAmbilData.get('detail_pesanan')


		detail_pesanan_dict = ast.literal_eval(detail_pesanan)
		detail_pesanan_list = list(detail_pesanan_dict.values())

		# detail_pesanan = detail_pesanan_list

		

		

		# print(type(detail_pesanan))

		# testing
		# last_pesanansiswa = PesananSiswa.select().order_by(PesananSiswa.id.desc()).get()
		# last_id = last_pesanansiswa.id
		# print(last_id)
		try:
			getidsiswa = Anak.get(Anak.id == id_siswa).id
		except Anak.DoesNotExist:
			return {"messages" : "id anak tidak ditemukan"}

		if getidsiswa == True:
			harga_total_int = int(harga_total)
			saldo_anak_byId = Anak.get(Anak.id == id_siswa).saldo
			if saldo_anak_byId >= harga_total_int:


				# Mengurangi saldo
				def decrement_saldo(harga_total, saldo):
					try:
				        # Mengurangi stok produk
						Anak.update(saldo=Anak.saldo - harga_total).where(Anak.id == id_siswa).execute()
						# print("saldo berhasil dikurangi.")
					except Exception as e:
						print(e)
				
				decrement_saldo(harga_total_int, saldo_anak_byId) 		

				pesanan_siswa = PesananSiswa.create(
					anak_id= id_siswa,
					totalPembayaran=harga_total,
					tanggal_pemesanan= date.today()
				)


				# query untuk mendapatkan id terakhir pesanansiswa
				last_pesanansiswa = PesananSiswa.select().order_by(PesananSiswa.id.desc()).get().id

				# merubah type data str ke dict
				detail_pesanan_str = detail_pesanan
				detail_pesanan_dict = eval(detail_pesanan_str)

				# pendefinisian ke type data dic
				detail_pesanan = detail_pesanan_dict

				# merubah dari type dict ke list
				detail_pesanan_list = []

				# looping untuk menjumlah 
				for key, value in detail_pesanan.items():
				    detail_pesanan_list.append({'pesanansiswa_id': last_pesanansiswa, **value})


				for data_dict in detail_pesanan_list:
					DetailPesanan.create(**data_dict)

				# Coba coba

				# def simpan_data_dummy(data):
				#     # Membuat objek PesananSiswa baru
				    

				#     # Menyimpan data detail pesanan

				#     for key in detail_pesanan:
				# 		data_order = detail_pesanan[key]
				# 		for data_detail_pesanan in data_order:
				# 		    # Admin diambil dari nama class table 
				# 		    DetailPesanan.create(**data_detail_pesanan)

				#     # for key, value in data['detail_pesanan']:
				#     #     DetailPesanan.create(
				#     #         pesanansiswa_id=last_id,
				#     #         kuantitas=value['kuantitas'],
				#     #         harga=value['harga'],
				#     #         namaproduk=value['namaproduk']
				#     #     )

				# simpan_data_dummy(parserAmbilData)

				# for key in detail_pesanan:
				# 	data_order = detail_pesanan[key]
				# 	for data_detail_pesanan in data_order:
				# 	    # Admin diambil dari nama class table 
				# 	    DetailPesanan.create(**data_detail_pesanan)

				# for detail_id, detail_data in detail_pesanan:
				# 	DetailPesanan.create(
			    #         pesanansiswa_id= last_id,
			    #         kuantitas=detail_data['kuantitas'],
			    #         harga=detail_data['harga'],
			    #         namaproduk=detail_data['namaproduk']
		        # )

				# for key in detail_pesanan:			
				# 	print(str(detail_pesanan[key]))
					# dataPesanan["pesanansiswa_id"] = last_id 

				# save = PesananSiswa.create(
				# 	anak_id = id_siswa,
				# 	totalPembayaran = harga_total,
				# 	ttl_pemesanan = date.today(),
				# )

				# for key in detail_pesanan:
				# 	last_pesanansiswa = PesananSiswa.select().order_by(PesananSiswa.id.desc()).get()
				# 	last_id = last_pesanansiswa.id
				# 	# dataPesanan = int(detail_pesanan[key])
				# 	# dataPesanan["pesanansiswa_id"] = last_id 

				# for key in detail_pesanan:
				# 	data_order = detail_pesanan[key]
				# 	for data_detail_pesanan in data_order:
				# 	    # Admin diambil dari nama class table 
				# 	    DetailPesanan.create(**data_detail_pesanan)
			else:
				messages = "Saldo tidak cukup"
		else:
			messages = "Id siswa tidak ditemukan"
		return {'messages': messages}


class Ceksaldo(Resource):
	def get(self):
		parserData = reqparse.RequestParser()
		parserData.add_argument('id_siswa')


		parserAmbilData = parserData.parse_args()
		id_siswa = parserAmbilData.get('id_siswa')


		query = Anak.select().where(Anak.id == id_siswa)

		datas = []

		for data in query:
			datas.append({
				"nama" : data.nama,
				"kelas" : data.kelas,
				"saldo" : data.saldo
				})

		return jsonify(datas)





@app.route('/')
def index():
    return "Go To the Moon"




# #####################  RESOURCE / ENDPOINT API ###################################


# ADMIN LOGIN & LOGOUT
api.add_resource(Loginadmin, '/api/login/', endpoint = 'login')
api.add_resource(logout, '/api/logout/', endpoint = 'logout')


# KARYAWAN LOGIN & LOGOUT
api.add_resource(Loginkaryawan, '/api/loginkaryawan/', endpoint = 'logintkaryawan')
api.add_resource(Logoutkaryawan, '/api/logoutkaryawan/', endpoint = 'logoutkaryawan')


# KARYAWAN
api.add_resource(Karyawans, '/api/karyawans', endpoint='karyawans')
api.add_resource(Karyawanbyid, '/api/karyawanbyid/<int:id>', endpoint='karyawanbyid')


# ORANGTUA LOGIN & LOGOUT
api.add_resource(Loginorangtua, '/api/loginorangtua/', endpoint = 'loginorangtua')
api.add_resource(Logoutorangtua, '/api/logoutorangtua/', endpoint = 'logoutorangtua')


# Histori Semua Pesanan Anak Berdasarkan Id Orang Tua
api.add_resource(Historipesanan, '/api/historipesanans/<int:orangtua_id>', endpoint='historipesanans')

# Menampilkan jumlah total saldo dari anak
api.add_resource(Totalsaldoanaks, '/api/totalsaldoanaks/<int:orangtua_id>', endpoint='totalsaldoanaks')

# Menampilkan total pembelian
api.add_resource(Totalpembelians, '/api/totalpembelians/<int:orangtua_id>', endpoint='totalpembelians')

# Menampilkan nama anak
api.add_resource(NamaAnak, '/api/namaanaks/<int:orangtua_id>', endpoint='namaanaks')

# Menampilkan data berdasarkan nama anak
api.add_resource(SearchDataByName, '/api/searchdatabynama/<int:orangtua_id>', endpoint='searchdatabynama')

# Menampilkan detail pesanan
api.add_resource(Detailpesanan, '/api/detailpesanan/<int:id_pesanan>', endpoint='detailpesanan')

# menampilkan data anak yang dimiliki orang tua
api.add_resource(Dataanak, '/api/dataanak/<int:orangtua_id>', endpoint='dataanak')

# Menampilkan data orang tua 
api.add_resource(Dataorangtua, '/api/dataorangtua/<int:orangtua_id>', endpoint='dataorangtua')

# Search histori pesanan by id
api.add_resource(SearchHistoriPesanan, '/api/searchHistoripesananbyid/', endpoint='searchHistoribyid')

# Menampilkan semua histori pesanan
api.add_resource(SemuaHistoriPesanan, '/api/semuahistoripesanan/', endpoint='semuahistoripesanan')

# Menampilkan semua produk
api.add_resource(Product, '/api/productall/', endpoint='productall')

# Menampilkan produk berdasarkan kategori
api.add_resource(ProductSearch, '/api/productsearch/', endpoint='productsearch')

# Mendapatkan product berdasarkan id untuk keranjang
api.add_resource(Getproductbyid, '/api/productbyid/<int:product_id>', endpoint='productbyid')

# Membuat pesanan
api.add_resource(Order, '/api/order/', endpoint='order')

# Menampilkan saldo beserta nama dan kelas anak 
api.add_resource(Ceksaldo, '/api/ceksaldo/', endpoint='ceksaldo')





if __name__== '__main__':
    app.run(
		host='0.0.0.0',
		debug='True',
		port=5055
	)