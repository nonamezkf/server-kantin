from flask import Flask, jsonify, session
from peewee import *
from flask_restful import Resource, Api, reqparse
from hashlib import sha256

import datetime

from peewee import *

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
	no_tlp = SmallIntegerField()
	join_at = DateTimeField(default=datetime.datetime.now())

class Anak(BaseModel):
	orangtua = ForeignKeyField(OrangTua, backref='anaks')
	nama = TextField()
	username = CharField()
	role = TextField()
	password = CharField()
	alamat = TextField()
	no_tlp = SmallIntegerField()
	saldo = IntegerField()
	tgl_lahir = DateField()

class Admin(BaseModel):
	role = TextField()
	nama = TextField()
	email = CharField()
	password = CharField()
	no_tlp = SmallIntegerField()

class Karyawan(BaseModel):
	admin = ForeignKeyField(Admin, backref='karyawans')
	nama = TextField()
	email = CharField()
	password = CharField()
	no_tlp = SmallIntegerField()

class PesananSiswa(BaseModel):
	anak = ForeignKeyField(Anak, backref='pesanansiswas')
	totalPembayaran = IntegerField()
	ttl_pemesanan = DateTimeField(default=datetime.datetime.now())

class DetailPesanan(BaseModel):
	pesanansiswa = ForeignKeyField(PesananSiswa, backref='detailpesanan')
	kuantitas = SmallIntegerField()
	harga = IntegerField()

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

# controlerlogin
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
			result = "gagal"
			return jsonify(result)
		else:
			admin_id = session['admin_id'] = admin.id
			auth_user = {
				"admin_id": admin_id
			}

			print(auth_user)
			# auth_user_admin(admin)
			# print(session['admin_id'])
			# result = "sukses"
			return {"message":"sukses", "auth_user":auth_user}

class logout(Resource):
	def get(self):
		parserData = reqparse.RequestParser()
		parserData.add_argument('session_hapus')
		parserAmbilData = parserData.parse_args()
		hapus_session = parserAmbilData.get('session_hapus')

		if hapus_session == True:
			session.pop('admin_id', None)

class Karyawans(Resource):
	def get(self):
		query = Karyawan.select()
		datas = []

		for row in query:
			datas.append({
				'id':row.id,
				'nama':row.nama,
				'email':row.email,
				'no_tlp':row.no_tlp
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
			admin = id_admin,
			nama = form_nama,
			email = form_email,
			no_tlp = form_no_tlp,
			password = form_password
		)

	# def put(self):
	# 	pass




class Karyawanbyid(Resource):
	def get(self,id):
		# query = Karyawan.select().where(Karyawan.id == id)

		# datas = {}
		# for row in query:
		# 	datas = {
		# 		'id':row.id,
		# 		'nama':row.nama,
		# 		'email':row.email,
		# 		'no_tlp':row.no_tlp
		# 	}
		
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

		query = Karyawan.update({Karyawan.admin:id_admin, Karyawan.nama:form_nama, Karyawan.email:form_email, Karyawan.no_tlp:form_no_tlp, Karyawan.password:form_password,}).where(Karyawan.id == id)
		query.execute()


@app.route('/')
def index():
    return "Go To the Moon"



api.add_resource(Loginadmin, '/api/login/', endpoint = 'login')
api.add_resource(logout, '/api/logout/', endpoint = 'logout')
api.add_resource(Karyawans, '/api/karyawans', endpoint='karyawans')
api.add_resource(Karyawanbyid, '/api/karyawanbyid/<int:id>', endpoint='karyawanbyid')


if __name__== '__main__':
    app.run(
		host='0.0.0.0',
		debug='True',
		port=5055
	)