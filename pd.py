
from peewee import *

DATABASE = SqliteDatabase('ecanteen.db')


db = SqliteDatabase('ecanteen.db')

class BaseModel(Model):
	class Meta:
		database = db

class users(BaseModel):
	username = TextField(unique=True)
	password = TextField()
	join_date = DateTimeField()

class products(BaseModel):
	id = AutoField()
	user = ForeignKeyField(users, backref='products')
	name = TextField()
	desc = TextField()
	price = IntegerField()
	quantity = IntegerField()
	category = TextField()
	image = TextField()

def create_tables():
	with db:
		db.create_tables([users, products])


